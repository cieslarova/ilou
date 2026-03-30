import pygame
import random

# --- Konstanty pro hru ---
# Základní rozměry monitorového okna hry
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700

# Rozměry samotného herního pole (kde padají kostky)
PLAY_WIDTH = 300  # Šířka 300px = 10 sloupců po 30px
PLAY_HEIGHT = 600 # Výška 600px = 20 řádků po 30px
BLOCK_SIZE = 30   # Velikost jedné herní kostičky (30x30 pixelů)

# Výpočet, kam se má horní levý roh herního pole vykreslit, aby byl hezky uprostřed obrazovky
TOP_LEFT_X = (SCREEN_WIDTH - PLAY_WIDTH) // 2
TOP_LEFT_Y = SCREEN_HEIGHT - PLAY_HEIGHT - 50

# --- Barvy (v RGB formátu pro Pygame) ---
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

# --- Tvary Tetromin (padajících objektů) ---
# Každý tvar představuje mřížku textu 5x5, kde '0' je pevný blok a '.' je vzduch.
# Pokud má tvar více vrstev (listů), jedná se pouze o jeho různé rotace.

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

# Seznamy všech tvarů a barev, které jim barevně odpovídají v indexovém pořadí
SHAPES = [S, Z, I, O, J, L, T]
SHAPE_COLORS = [GREEN, RED, CYAN, YELLOW, ORANGE, BLUE, PURPLE]

class Tetromino:
    """Reprezentuje jeden fyzický herní kámen. Pamatuje si svou pozici, tvar a aktuální rotaci."""
    def __init__(self, x, y, shape):
        self.x = x # Virtuální souřadnice na hrací desce (0 až 9)
        self.y = y # Virtuální souřadnice pádu (0 až 19)
        self.shape = shape
        self.color = SHAPE_COLORS[SHAPES.index(shape)] # Najde odpovídající barvu
        self.rotation = 0 # Výchozí rotace (vždy první obrázek ze seznamu)

    def get_shape(self):
        """Pomocí zbytku po dělení sjednocuje nekonečné klikání rotace na platný index obrázku."""
        return self.shape[self.rotation % len(self.shape)]

class Board:
    """Třída na spravování rozměrů hrací plochy a kreslení usazených bloků."""
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = self.create_grid({})

    def create_grid(self, locked_positions):
        """Pokaždé když se pohne hra, vykreslí herní mřížku znovu z černé barvy a následně do ní nakreslí spadané bloky."""
        # Udělá celé hrací pole jako obří dvourozměrný seznam ČERNÝCH polí 
        grid = [[BLACK for _ in range(self.width)] for _ in range(self.height)]

        # Vybarví jednotlivé usazené cihly barvou uloženou v paměti slovníku
        for i in range(self.height):
            for j in range(self.width):
                if (j, i) in locked_positions:
                    barva = locked_positions[(j, i)]
                    grid[i][j] = barva
        return grid

    def draw(self, surface):
        """Převede hrubá data tabulky na reálné barevné plošky a nakreslí ohraničení."""
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(surface, self.grid[i][j], (TOP_LEFT_X + j * BLOCK_SIZE, TOP_LEFT_Y + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

        # Čáry pro nakreslení estetické šachovnicové sítě (v pruzích)
        for i in range(self.height):
            pygame.draw.line(surface, GRAY, (TOP_LEFT_X, TOP_LEFT_Y + i * BLOCK_SIZE), (TOP_LEFT_X + PLAY_WIDTH, TOP_LEFT_Y + i * BLOCK_SIZE))
            for j in range(self.width):
                pygame.draw.line(surface, GRAY, (TOP_LEFT_X + j * BLOCK_SIZE, TOP_LEFT_Y), (TOP_LEFT_X + j * BLOCK_SIZE, TOP_LEFT_Y + PLAY_HEIGHT))

        # Tlustý červený okraj hrací desky
        pygame.draw.rect(surface, RED, (TOP_LEFT_X, TOP_LEFT_Y, PLAY_WIDTH, PLAY_HEIGHT), 5)

class Game:
    """Mozek celé hry. Drží pravidla o kolizích, skóre, herním čase a padání kostek."""
    def __init__(self):
        self.board = Board(10, 20)
        self.current_piece = self.new_piece() # Tohle právě letí vzduchem
        self.next_piece = self.new_piece()    # Tohle se objeví v miniatuře pro "příští blok"
        self.locked_positions = {} # Trvalá paměť pro už zapadlé kostky
        self.score = 0
        self.game_over = False

    def new_piece(self):
        """Vyplivne do obrazovky doprostřed nahoře úplně náhodné Tetromino."""
        return Tetromino(self.board.width // 2 - 2, 0, random.choice(SHAPES))

    def convert_shape_format(self, piece):
        """Ta nejdůležitější překladová funkce matice 5x5 -> na skutečné herní souřadnice kostiček."""
        positions = []
        format_shape = piece.get_shape() # Přečteme řetězec 5x5 pro konkrétní rotaci

        # Zjistíme kde v těch textech je napsaná Vytvořená Část (Nula)
        for i, line in enumerate(format_shape):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    positions.append((piece.x + j, piece.y + i))

        # Náš tvar je na matici 5x5 posunutý víc doleva a dolů, aby se otáčel přirozeně, proto ho zarovnáme pro hráče blíž kurzoru
        for i, pos in enumerate(positions):
            positions[i] = (pos[0] - 2, pos[1] - 4)

        return positions

    def valid_space(self, piece):
        """Vyhodnocuje fyzikální narážení bloku do stěn i už existujících podlah."""
        # Seznam prázdných míst v celém vesmíru pole (barva BLOCK = BLACK)
        accepted_pos = [[(j, i) for j in range(10) if self.board.grid[i][j] == BLACK] for i in range(20)]
        accepted_pos = [j for sub in accepted_pos for j in sub] # Konverze na jedno mega-pole čísel

        formatted = self.convert_shape_format(piece) # Spočítání aktuálního dotazu

        for pos in formatted:
            # Pokud chci jít na souřadnice, o kterých v seznamu prázdných míst nevědí... Tím pádem narážím.
            if pos not in accepted_pos:
                if pos[1] > -1: # Ignorujeme zplození kostky o chlup víš než je strop (tam srážka s okolním světem nevadí)
                    return False
        return True

    def check_lost(self):
        """Hra končí, jakmile mi aspoň jediná usazená kostka přeplnila kapacitu na osu Y < 1."""
        for pos in self.locked_positions:
            _, y = pos
            if y < 1: 
                return True
        return False

    def clear_rows(self):
        """Algoritmus ničící kostky složené hráči zespoda nahoru a udělující body."""
        inc = 0     # Odstraněné počty
        ind = -1    # Na jakém Y byl odstraněn poslední vrchní pruh
        
        # Pojedeme od Y = 19 k Y = 0 (zdola nahoru)
        for i in range(len(self.board.grid) - 1, -1, -1):
            row = self.board.grid[i]
            # Pokud v řádku neobjevím tu ČERNOU barvu (prázdnotu), tak je složený!
            if BLACK not in row:
                inc += 1
                ind = i
                # Odstranění stěny bloku
                for j in range(len(row)):
                    try:
                        del self.locked_positions[(j, i)]
                    except KeyError:
                        continue

        # Vynechat se má jen tehdy, když jsme zničili nějaké řady = Vznikly propasti bez gravitace 
        if inc > 0:
            # Každou přeživší kostku nad námi vezmi a propadni o "inc" řádků dolů
            # Musíme třídit bloky (od y nejspodnějšího z prvního propadajícího), ať kostkami nepřepisujeme patra pod námi v průběhu
            for key in sorted(list(self.locked_positions), key=lambda x: x[1])[::-1]:
                x, y = key
                if y < ind: # Jsi nad odstraněným řádkem? Přidám gravitaci! 
                    newKey = (x, y + inc) # Y ti posunu níž  
                    # Na tvou novou pozici vložím tvoje barvy, ze staré tě odpáruju
                    self.locked_positions[newKey] = self.locked_positions.pop(key)
            
            # Násobič bodů za smazání víc řad zaráz
            self.score += inc * 10 * inc

    def draw_text_middle(self, surface, text, size, color):
        """Malá pomocná funkce napsaná pro rendering titulků na konec hry jako 'Game Over'."""
        font = pygame.font.SysFont('comicsans', size, bold=True)
        label = font.render(text, 1, color)
        surface.blit(label, (TOP_LEFT_X + PLAY_WIDTH/2 - (label.get_width() / 2), TOP_LEFT_Y + PLAY_HEIGHT/2 - label.get_height()/2))

    def draw(self, surface):
        """Funkce spravující veškeré vykreslení a rozložení vizuálních prvků do Pygame plátna."""
        surface.fill(BLACK) # Nový čistý černý rámček (nutné pro plynulý chod u animací 2D)

        pygame.font.init()
        font = pygame.font.SysFont('comicsans', 60)
        label = font.render('TETRIS', 1, WHITE)
        surface.blit(label, (TOP_LEFT_X + PLAY_WIDTH / 2 - (label.get_width() / 2), 30)) # Velký nadpis 

        font = pygame.font.SysFont('comicsans', 30)
        
        # Bodovací štítek vpravo
        score_label = font.render(f'Skóre: {self.score}', 1, WHITE)
        sx = TOP_LEFT_X + PLAY_WIDTH + 50
        sy = TOP_LEFT_Y + PLAY_HEIGHT/2 - 100
        surface.blit(score_label, (sx, sy))

        # Odkrytí miniatury aktuálně drženého nadcházejícího tvru
        next_label = font.render('Další tvar:', 1, WHITE)
        surface.blit(next_label, (sx, sy + 160))
        
        # Ruční částečný render mini tvru vedle herní zóny (aby ho hráč viděl na displeji vedle sebe, a ne ve hře)
        format_shape = self.next_piece.shape[self.next_piece.rotation % len(self.next_piece.shape)]
        for i, line in enumerate(format_shape):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    pygame.draw.rect(surface, self.next_piece.color, (sx + j*BLOCK_SIZE, sy + 200 + i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

        # Volání kreslení pro Board mřížku
        self.board.grid = self.board.create_grid(self.locked_positions)
        self.board.draw(surface)

        # Kostka neustále padající aktuálně dolů – musí se malovat až na jako poslední úplný vršek přes tabulku 
        piece_pos = self.convert_shape_format(self.current_piece)
        for i in range(len(piece_pos)):
            x, y = piece_pos[i]
            if y > -1:
                pygame.draw.rect(surface, self.current_piece.color, (TOP_LEFT_X + x * BLOCK_SIZE, TOP_LEFT_Y + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

        pygame.display.update()

def main():
    """Hlavní smyčka Fáze 2 ovládá rychlost pádu, klávesnici a průběžný tok aplikace."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Tetris - Fáze 2')
    
    game = Game()
    clock = pygame.time.Clock()
    
    fall_time = 0     # Časovač k pádu na ose Y (mili-sekundy limit)
    fall_speed = 0.27 # Rychlost pádu na ose (270ms v sekundě se drcne o Y - 1)
    
    run = True
    while run:
        # Pokaždé přebarvi svět podle kostek uvězněných dole 
        game.board.grid = game.board.create_grid(game.locked_positions)
        
        fall_time += clock.get_rawtime()
        clock.tick() 

        # Auto-pád
        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            game.current_piece.y += 1
            # Odraz a zachycení konce pádu - Jsem už moc natvrdo zapasovaný v trvalém boxu = Kostka tam končí svou pouť!
            if not (game.valid_space(game.current_piece)) and game.current_piece.y > 0:
                game.current_piece.y -= 1
                change_piece = True
            else:
                change_piece = False

        # Odchyt událostí ovladače a klávesnice.
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Uživatel klikl na křížek Windowsního okna
                run = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                # Na každý směr je ochrana -> provedeme pohyb a kdyby způsoboval kolizi se stěnou nebo usazenými bloky, hned ho vrátíme zpět (+/- šipkami).
                if event.key == pygame.K_LEFT: 
                    game.current_piece.x -= 1
                    if not game.valid_space(game.current_piece): 
                        game.current_piece.x += 1
                elif event.key == pygame.K_RIGHT: 
                    game.current_piece.x += 1
                    if not game.valid_space(game.current_piece): 
                        game.current_piece.x -= 1
                elif event.key == pygame.K_DOWN: 
                    game.current_piece.y += 1   # Přidání Y = Padáme Rychleji!
                    if not game.valid_space(game.current_piece):
                        game.current_piece.y -= 1
                elif event.key == pygame.K_UP: 
                    game.current_piece.rotation += 1 # Otočením kostky se změní tvar
                    if not game.valid_space(game.current_piece): # Pokud je otočený tvar nepřijatelný, protáčíme zpět! 
                        game.current_piece.rotation -= 1

        piece_pos = game.convert_shape_format(game.current_piece)
        
        # Tato část uzavírá kruh pro uzamčení spadnuvšího objektu do hry
        if 'change_piece' in locals() and change_piece:
            for pos in piece_pos:
                p = (pos[0], pos[1])
                # Každý z kousků, kterými disponoval právě spadený velký tvar (4 kostičky) hodíme samostatně obarvené do trvalého Dictionary na mapě.
                game.locked_positions[p] = game.current_piece.color
            
            # Další kostka letí do akce z fronty, a fronta si tahá novou z pytlíků
            game.current_piece = game.next_piece
            game.next_piece = game.new_piece()
            change_piece = False
            
            # Okamžitá kontrola složených obrovských staveb po dopadu bloku
            game.clear_rows()

        # Nech vykreslit plátno
        game.draw(screen)

        # GAME OVER Check - Hráč poskládal nepřekonatelnou horu ke stropu.
        if game.check_lost():
            game.draw_text_middle(screen, "Game Over", 80, WHITE)
            pygame.display.update()
            pygame.time.delay(1500) # Malé zamrznutí a pláč nad neúspěchem hráče, ihned potom hra crashne / spadne. 
            run = False

if __name__ == '__main__':
    main()
