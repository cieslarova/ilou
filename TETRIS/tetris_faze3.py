import pygame
import random
import os

# --- Konstanty pro hru ---
# Základní rozměry herního monitoru okna
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
PLAY_WIDTH = 300  
PLAY_HEIGHT = 600  
BLOCK_SIZE = 30

TOP_LEFT_X = (SCREEN_WIDTH - PLAY_WIDTH) // 2
TOP_LEFT_Y = SCREEN_HEIGHT - PLAY_HEIGHT - 50

# Paleta základních barev (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)

# --- Tvary Tetromin (Padajících tvarů reprezentovaných textovou maticí 5x5) ---
S = [['.....', '.....', '..00.', '.00..', '.....'],
     ['.....', '..0..', '..00.', '...0.', '.....']]

Z = [['.....', '.....', '.00..', '..00.', '.....'],
     ['.....', '...0.', '..00.', '..0..', '.....']]

I = [['.....', '..0..', '..0..', '..0..', '..0..'],
     ['.....', '0000.', '.....', '.....', '.....']]

O = [['.....', '.....', '.00..', '.00..', '.....']]

J = [['.....', '.0...', '.000.', '.....', '.....'],
     ['.....', '..00.', '..0..', '..0..', '.....'],
     ['.....', '.....', '.000.', '...0.', '.....'],
     ['.....', '..0..', '..0..', '.00..', '.....']]

L = [['.....', '...0.', '.000.', '.....', '.....'],
     ['.....', '..0..', '..0..', '..00.', '.....'],
     ['.....', '.....', '.000.', '.0...', '.....'],
     ['.....', '.00..', '..0..', '..0..', '.....']]

T = [['.....', '..0..', '.000.', '.....', '.....'],
     ['.....', '..0..', '..00.', '..0..', '.....'],
     ['.....', '.....', '.000.', '..0..', '.....'],
     ['.....', '..0..', '.00..', '..0..', '.....']]

SHAPES = [S, Z, I, O, J, L, T]
SHAPE_COLORS = [GREEN, RED, CYAN, YELLOW, ORANGE, BLUE, PURPLE]

class Tetromino:
    """Třída na držení paměťových metadat o jediné momentálně padajicí kostce z oblohy."""
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = SHAPE_COLORS[SHAPES.index(shape)]
        self.rotation = 0

    def get_shape(self):
        """Zabezpečuje správný výběr rotace pro matice tvarů i v případě 20+ zmáčknutí rotace hráčem díky Modulo funkci."""
        return self.shape[self.rotation % len(self.shape)]

class Board:
    """Stavba a vykreslování hrací krabice a pozadí pro uchycené statické bloky (Mřížky)."""
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = self.create_grid({})

    def create_grid(self, locked_positions):
        """Nový 2D list pro neustále překreslující se Pygame obsahující černo, do kterého následně lepíme spadené kostky."""
        grid = [[BLACK for _ in range(self.width)] for _ in range(self.height)]
        for i in range(self.height):
            for j in range(self.width):
                if (j, i) in locked_positions:
                    barva = locked_positions[(j, i)]
                    grid[i][j] = barva
        return grid

    def draw(self, surface):
        """Vyplňuje fyzicky hrubé X, Y souřadnice na vizuální čtverečky do vizuálního okna (pygame.draw.rect)."""
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(surface, self.grid[i][j], (TOP_LEFT_X + j * BLOCK_SIZE, TOP_LEFT_Y + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

        # Tenoučké mřížkové šedivé šáchovnicové linky na pozadí, ať poznáme, do jakého sloupce se strefujeme.
        for i in range(self.height):
            pygame.draw.line(surface, GRAY, (TOP_LEFT_X, TOP_LEFT_Y + i * BLOCK_SIZE), (TOP_LEFT_X + PLAY_WIDTH, TOP_LEFT_Y + i * BLOCK_SIZE))
            for j in range(self.width):
                pygame.draw.line(surface, GRAY, (TOP_LEFT_X + j * BLOCK_SIZE, TOP_LEFT_Y), (TOP_LEFT_X + j * BLOCK_SIZE, TOP_LEFT_Y + PLAY_HEIGHT))

        pygame.draw.rect(surface, RED, (TOP_LEFT_X, TOP_LEFT_Y, PLAY_WIDTH, PLAY_HEIGHT), 5)

class Game:
    """Mozek hry sdružující mřížku Board, letící tvary (Tetrino) a zpracovávající zadané skóre a bodový příděl."""
    def __init__(self, player_name=""):
        self.board = Board(10, 20)
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()
        self.locked_positions = {}
        self.score = 0
        self.game_over = False
        self.player_name = player_name

    def new_piece(self):
        """Rychlý zplošťovač posílající nový náhodný kámen nahoru pod strop."""
        return Tetromino(self.board.width // 2 - 2, 0, random.choice(SHAPES))

    def convert_shape_format(self, piece):
        """Transfomuje nesmyslnou 'S' mřížku teček na logické body X a Y, na kterých mají být dlaždičky a kudy nemůžou projít jinými tvary."""
        positions = []
        format_shape = piece.get_shape()

        for i, line in enumerate(format_shape):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    positions.append((piece.x + j, piece.y + i))

        # Modifikace offsetu proti těžišti 5x5 tak, aby uživatel klikal skutečně kurzorem doprostřed!
        for i, pos in enumerate(positions):
            positions[i] = (pos[0] - 2, pos[1] - 4)

        return positions

    def valid_space(self, piece):
        """Kolizní scanner napříč celou plochou. Kontroluje, zda kostka právě nenarazila hlavou do stěny nebo zadku jiné kostky."""
        # Sebere všechny existující absolutně černá pole 
        accepted_pos = [[(j, i) for j in range(10) if self.board.grid[i][j] == BLACK] for i in range(20)]
        accepted_pos = [j for sub in accepted_pos for j in sub]

        formatted = self.convert_shape_format(piece) 

        # Pokud se bod Tetromina protne s něčím co NENÍ uvedené na černém seznamu (volných zónách), tak tam nemůže!
        for pos in formatted:
            if pos not in accepted_pos:
                if pos[1] > -1: # Ignorace čerstvě se rodících bloků tam nahoře přes Y <= 0!
                    return False
        return True

    def check_lost(self):
        """Smrtící kontrola hledající libovolný kámen, který přečuhuje Y osu směrem nahoru."""
        for pos in self.locked_positions:
            _, y = pos
            if y < 1: 
                return True
        return False

    def clear_rows(self):
        """Hledání plných zabarvených čar a gravitace padajicích umazaných řad shora dolů."""
        inc = 0
        ind = -1
        # Projíždí všechny řádky podél patra. OD SPODKU, k Vršku (-1 úbytek i)
        for i in range(len(self.board.grid) - 1, -1, -1):
            row = self.board.grid[i]
            if BLACK not in row: # Ani políčko černé prázdnoty! Tohle je trefa. Cílem je zničit blok
                inc += 1
                ind = i
                # Projedeme a vydloubneme ze slovníku celou barevnou stěnu dotčenou i. řádkem.
                for j in range(len(row)):
                    try:
                        del self.locked_positions[(j, i)]
                    except KeyError:
                        continue

        # Gravitační posun propasti co právě Vznikla mezi ind řádkem
        if inc > 0:
            # Vezmeme to opět řazeně (Obráceným seřazením podle Y!), abychom nepsali na pole kostkám co na pád Teprve čekají o pár cyklů hlouběji.
            for key in sorted(list(self.locked_positions), key=lambda x: x[1])[::-1]:
                x, y = key
                if y < ind: # Visíme nad mezerou propasti
                    newKey = (x, y + inc) # Šoupeme gravitační osu bloku
                    self.locked_positions[newKey] = self.locked_positions.pop(key)
            
            # Bonifikace obřího kassa za 3 - 4 řádky rázem dole
            self.score += inc * 10 * inc

    def draw_text_middle(self, surface, text, size, color):
        font = pygame.font.SysFont('comicsans', size, bold=True)
        label = font.render(text, 1, color)
        surface.blit(label, (TOP_LEFT_X + PLAY_WIDTH/2 - (label.get_width() / 2), TOP_LEFT_Y + PLAY_HEIGHT/2 - label.get_height()/2))

    def draw(self, surface):
        """Místo v paměti kde vizuální Engine obkresluje celou hru. Zde malujeme panely mimo box hráčů, jako Skóre / Jména a Next Queue obdélníky."""
        surface.fill(BLACK) 

        pygame.font.init()
        font = pygame.font.SysFont('comicsans', 60)
        label = font.render('TETRIS', 1, WHITE)
        surface.blit(label, (TOP_LEFT_X + PLAY_WIDTH / 2 - (label.get_width() / 2), 30))

        font = pygame.font.SysFont('comicsans', 30)
        
        # Sekce Fáze 3: Titulek uživatele z paměti Input boxu (jméno) poslané při startu main()
        player_label = font.render(f'Hráč: {self.player_name}', 1, YELLOW)
        sx = TOP_LEFT_X + PLAY_WIDTH + 50
        sy = TOP_LEFT_Y + PLAY_HEIGHT/2 - 100
        surface.blit(player_label, (sx, sy - 50))
        
        # Bodovací label vpravo
        score_label = font.render(f'Skóre: {self.score}', 1, WHITE)
        surface.blit(score_label, (sx, sy))

        # Box na preview nejbližší padajicí zkázy (Zobrazený vpravo)
        next_label = font.render('Další tvar:', 1, WHITE)
        surface.blit(next_label, (sx, sy + 160))
        
        format_shape = self.next_piece.shape[self.next_piece.rotation % len(self.next_piece.shape)]
        for i, line in enumerate(format_shape):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    pygame.draw.rect(surface, self.next_piece.color, (sx + j*BLOCK_SIZE, sy + 200 + i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

        self.board.grid = self.board.create_grid(self.locked_positions)
        self.board.draw(surface)

        piece_pos = self.convert_shape_format(self.current_piece)
        for i in range(len(piece_pos)):
            x, y = piece_pos[i]
            if y > -1:
                pygame.draw.rect(surface, self.current_piece.color, (TOP_LEFT_X + x * BLOCK_SIZE, TOP_LEFT_Y + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

        pygame.display.update()

# --- Funkce fází 3: Skóre, Pauza, Menu ---
def ziskej_skore():
    """Fce pro bezpečné vyčtení externího databázového .txt souboru na místním C:\ disku. Vyřadí navíc vše pod Top 3."""
    skore_cesta = os.path.join(os.path.dirname(__file__), "skore.txt")
    if not os.path.exists(skore_cesta): # Nejsou body? Asi instaloval hru poprvé, jdeme zpět z prázdnou a čistou.
        return []
    try:
        with open(skore_cesta, "r", encoding="utf-8") as f:
            lines = f.readlines()
            skore_list = []
            for line in lines:
                parts = line.strip().split(",") # Uloženo jako Jan,510
                if len(parts) == 2:
                    skore_list.append((parts[0], int(parts[1]))) # Otypujeme string na Integer u čísla bodů kvůli třídění dole
            # Lamba - seřadí lidi dle [1] (bodíky) klesajíc (Reverse = nejlepší nahoře). Poté ořeže pro [:3] – ukáže TOP3 
            return sorted(skore_list, key=lambda x: x[1], reverse=True)[:3]
    except (OSError, ValueError):
        return [] # Ochrana proti pádu v případě náladových OS práv Windows systému, chybného editování userem.. apod

def uloz_skore(jmeno, skore):
    """Získává staré uložení skóre, porovná nový záznam jména, seřadí do top 3 a silově natlačí ty nejlepší data čistě zpět na disk file."""
    skore_list = ziskej_skore()
    skore_list.append((jmeno, skore))
    skore_list = sorted(skore_list, key=lambda x: x[1], reverse=True)[:3]
    skore_cesta = os.path.join(os.path.dirname(__file__), "skore.txt")
    try:
        with open(skore_cesta, "w", encoding="utf-8") as f: # Režim "w" smaže natrvalo starý obsah a nahradí novými řadami top hráčů 
            for jm, points in skore_list:
                f.write(f"{jm},{points}\n")
    except (OSError, ValueError):
        pass

def pauza(screen):
    """Vymrští hlavní Game okno do menší umělé smyčky čekajicí pouze na mačknutí Space-baru k opuštění této bariéry a návratu do hry (čas hry je tím zastaven)."""
    font = pygame.font.SysFont('comicsans', 60, bold=True)
    label = font.render("PAUZA", 1, WHITE)
    screen.blit(label, (TOP_LEFT_X + PLAY_WIDTH/2 - (label.get_width() / 2), TOP_LEFT_Y + PLAY_HEIGHT/2 - label.get_height()/2))
    pygame.display.update()
    
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = False

def zobraz_menu(screen):
    """Předsunutá vstupní grafická Fáze 3 obsluha určená výhradně k získání Name argumentu z okna před spuštěním hry uživatelem (Enterem)."""
    run = True
    jmeno = "" # Buffer jména napojený na obří string Pygame blit Text.
    font = pygame.font.SysFont('comicsans', 40)
    title_font = pygame.font.SysFont('comicsans', 70, bold=True)
    
    while run:
        screen.fill(BLACK)
        title = title_font.render("TETRIS", 1, WHITE)
        screen.blit(title, (SCREEN_WIDTH/2 - title.get_width()/2, 100))
        
        inst1 = font.render("Šipky - pohyb a rotace", 1, GRAY)
        inst2 = font.render("Mezerník - pauza", 1, GRAY)
        screen.blit(inst1, (SCREEN_WIDTH/2 - inst1.get_width()/2, 250))
        screen.blit(inst2, (SCREEN_WIDTH/2 - inst2.get_width()/2, 300))
        
        prompt = font.render("Zadej své jméno:", 1, WHITE)
        screen.blit(prompt, (SCREEN_WIDTH/2 - prompt.get_width()/2, 400))
        
        name_lbl = font.render(jmeno + "_", 1, YELLOW)
        screen.blit(name_lbl, (SCREEN_WIDTH/2 - name_lbl.get_width()/2, 450))
        
        start_lbl = font.render("Stiskni ENTER pro start", 1, GREEN)
        screen.blit(start_lbl, (SCREEN_WIDTH/2 - start_lbl.get_width()/2, 550))
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: # Akce Start Buttonu zapnout padání v hlavní loopě Game
                    if len(jmeno) > 0:
                        return jmeno           # Vrať hlavní smyčce to hotové vyplněné jméno
                elif event.key == pygame.K_BACKSPACE: # Akce gumování překliků psaní
                    jmeno = jmeno[:-1]
                else:
                    if len(jmeno) < 15 and event.unicode.isprintable(): # Neumožníme dlouhý a sprostý Unicode texty ani zrůdnosti co zničí screen pole 
                        jmeno += event.unicode

def herni_smycka(screen, jmeno_hrace):
    """Jádro programu odštěpené ze staré hlavní main(). Obsluha všeho v reálném čase, dokud nepřijde kolaps nebo úmrtí."""
    game = Game(jmeno_hrace)
    clock = pygame.time.Clock()
    
    fall_time = 0     
    fall_speed = 0.27 
    
    run = True
    while run:
        game.board.grid = game.board.create_grid(game.locked_positions)
        
        fall_time += clock.get_rawtime()
        clock.tick() 

        # Logika pádu – přichází rychlá smrt.
        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            game.current_piece.y += 1 # Auto posun gravitace
            # Nejsou tam volné stěny! Narazil ten Tvar? Vrať tělo zpátky a zamkni proces. (change piece)
            if not (game.valid_space(game.current_piece)) and game.current_piece.y > 0:
                game.current_piece.y -= 1
                change_piece = True
            else:
                change_piece = False

        # Event controller Fáze 3 okna.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN: # Hráč interaguje
                if event.key == pygame.K_SPACE:  
                    pauza(screen) # Pozvi okno ke sledování pouze K_SPACE klíče ve funkci a zamraž vše ostatní ve While
                elif event.key == pygame.K_LEFT: 
                    game.current_piece.x -= 1
                    if not game.valid_space(game.current_piece): # Kolizní ochrana na stěny krabice!
                        game.current_piece.x += 1
                elif event.key == pygame.K_RIGHT: 
                    game.current_piece.x += 1
                    if not game.valid_space(game.current_piece): 
                        game.current_piece.x -= 1
                elif event.key == pygame.K_DOWN: 
                    game.current_piece.y += 1
                    if not game.valid_space(game.current_piece):
                        game.current_piece.y -= 1
                elif event.key == pygame.K_UP: 
                    game.current_piece.rotation += 1
                    if not game.valid_space(game.current_piece): 
                        game.current_piece.rotation -= 1

        piece_pos = game.convert_shape_format(game.current_piece)
        
        # Zvrat na change piece -> tělo se obkresluje napevno a tvoříme nové padající z oblohy z Queue čekaček
        if 'change_piece' in locals() and change_piece:
            for pos in piece_pos:
                p = (pos[0], pos[1])
                game.locked_positions[p] = game.current_piece.color
            
            game.current_piece = game.next_piece
            game.next_piece = game.new_piece()
            change_piece = False
            
            game.clear_rows() # Uklízení řádků

        game.draw(screen)

        if game.check_lost():
            game.draw(screen) 
            uloz_skore(jmeno_hrace, game.score) # Umřeli jsme... ale zapíše se naší námaha na .txt file do soukromí u hráče !
            
            # Kreslení smutečního obřadu / Death screen na prostředek s černým krytem pro čitelnost nad mrtvými kostkami vzadu.
            pygame.draw.rect(screen, BLACK, (TOP_LEFT_X + 10, TOP_LEFT_Y + PLAY_HEIGHT//2 - 170, PLAY_WIDTH - 20, 360))
            pygame.draw.rect(screen, WHITE, (TOP_LEFT_X + 10, TOP_LEFT_Y + PLAY_HEIGHT//2 - 170, PLAY_WIDTH - 20, 360), 3)
            
             
            game.draw_text_middle(screen, "Game Over", 50, WHITE)
            
            pygame.display.update()
            pygame.time.delay(500) 
            
            font = pygame.font.SysFont('comicsans', 30)
            
            # Rozpisování Výpovědí na stěny o body + TOP3 řádky 
            y_offset = TOP_LEFT_Y + PLAY_HEIGHT//2 - 10
            lbl_b = font.render(f"Získal jsi: {game.score}", 1, GREEN)
            screen.blit(lbl_b, (TOP_LEFT_X + PLAY_WIDTH//2 - lbl_b.get_width()//2, y_offset))
            y_offset += 40
            
            lbl_m = font.render("Top 3 Rekordy:", 1, YELLOW)
            screen.blit(lbl_m, (TOP_LEFT_X + PLAY_WIDTH//2 - lbl_m.get_width()//2, y_offset))
            y_offset += 35
            
            # Přečti ze souboru co jsme tam reálně teď nakrmili
            skore_list = ziskej_skore()
            for i, (jm, bod) in enumerate(skore_list):
                txt = f"{i+1}. {jm} - {bod}" # String Format Výpisovka jako pro školní lavice
                lbl_s = font.render(txt, 1, WHITE)
                screen.blit(lbl_s, (TOP_LEFT_X + PLAY_WIDTH//2 - lbl_s.get_width()//2, y_offset))
                y_offset += 30
            
            lbl_n = font.render("M - Menu | R - Restart", 1, CYAN)
            screen.blit(lbl_n, (TOP_LEFT_X + PLAY_WIDTH//2 - lbl_n.get_width()//2, y_offset + 20))    
            
            pygame.display.update()
            
            # Cekáni na prohrané obrazovce do chvíle než si uživatel promyslí stisk volby přes R, a nebo Menu M klávesy!!
            waiting = True
            while waiting:
                for ev in pygame.event.get():
                    if ev.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    if ev.type == pygame.KEYDOWN:
                        if ev.key == pygame.K_r: # OK, hrajeme dál z fleku.
                            return 'restart'
                        if ev.key == pygame.K_m: # Konec práce. Jdeme si měnit Input Jména z Hlavního.
                            return 'menu'
            run = False

def main():
    """Vrchní Vládce Architektury všech smyček - nedělá nic krom delegace smluv do vedlejších okruhů! (Řízena Návraty Fází)"""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Tetris - Fáze 3')
    
    while True: # Nezničitelně žijící okno
        hrac = zobraz_menu(screen) # Počkáme dokud nemáme v ruce platný return na String nového jména od Hráče uvnitř boxíků..  
        akce = 'restart'
        while akce == 'restart':
            akce = herni_smycka(screen, hrac) # Hráč buď vrátil R(estart), M(enu), nebo kill okna!
            if akce == 'menu': # Uf, chceme ven od hraní. Zníčí se smyčka a vrátíme cyklus poletování do toho While True Zobraz_Menu nad námi!
                break

if __name__ == '__main__':
    main()
