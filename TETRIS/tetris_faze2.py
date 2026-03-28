import pygame
import random

# --- Konstanty pro hru ---
# Rozměry obrazovky a hrací plochy
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
PLAY_WIDTH = 300  # 10 sloupců * 30 pixelů = 300
PLAY_HEIGHT = 600  # 20 řádků * 30 pixelů = 600
BLOCK_SIZE = 30

# Pozice levého horního rohu hrací plochy (vycentrováno na střed)
TOP_LEFT_X = (SCREEN_WIDTH - PLAY_WIDTH) // 2
TOP_LEFT_Y = SCREEN_HEIGHT - PLAY_HEIGHT - 50

# Barvy použité ve hře (RGB formát)
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

# --- Tvary Tetromin ---
# Definice jednotlivých tvarů kostek a jejich rotací
# '0' reprezentuje plný blok, '.' reprezentuje prázdný prostor v matici 5x5
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

# Globální seznamy tvarů a barev k nim příslušících
SHAPES = [S, Z, I, O, J, L, T]
SHAPE_COLORS = [GREEN, RED, CYAN, YELLOW, ORANGE, BLUE, PURPLE]

class Tetromino:
    """
    Třída reprezentující jeden padající blok. 
    Uskladňuje si svou pozici v mřížce (X a Y), aktuální tvar a rotaci.
    """
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        # Barva je určena podle indexu tvaru v seznamu SHAPES
        self.color = SHAPE_COLORS[SHAPES.index(shape)]
        self.rotation = 0  # Vychozí stav rotace

    def get_shape(self):
        """Metoda pro získání matice aktuálního zobrazení kostky ze seznamu rotací."""
        return self.shape[self.rotation % len(self.shape)]

class Board:
    """
    Správce hrací plochy, který uchovává vizuální podobu spadených kostek.
    """
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # Původní prázdná mřížka
        self.grid = self.create_grid({})

    def create_grid(self, locked_positions):
        """
        Vytvoří a vrátí mřížku pro renderování kostek. 
        Proměnná locked_positions představuje slovník zamčených kostek.
        """
        # Inicializace čisté mřížky pozadí na černou barvu
        grid = [[BLACK for _ in range(self.width)] for _ in range(self.height)]

        # Vyplnění mřížky barvami dřívějších (usazených) kostek
        for i in range(self.height):
            for j in range(self.width):
                if (j, i) in locked_positions:
                    barva = locked_positions[(j, i)]
                    grid[i][j] = barva
        return grid

    def draw(self, surface):
        """Vykreslení samotné hrací plochy a zaplněných pozic."""
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(surface, self.grid[i][j], (TOP_LEFT_X + j * BLOCK_SIZE, TOP_LEFT_Y + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

        # Čáry pro přehlednou šachovnici na hrací ploše
        for i in range(self.height):
            pygame.draw.line(surface, GRAY, (TOP_LEFT_X, TOP_LEFT_Y + i * BLOCK_SIZE), (TOP_LEFT_X + PLAY_WIDTH, TOP_LEFT_Y + i * BLOCK_SIZE))
            for j in range(self.width):
                pygame.draw.line(surface, GRAY, (TOP_LEFT_X + j * BLOCK_SIZE, TOP_LEFT_Y), (TOP_LEFT_X + j * BLOCK_SIZE, TOP_LEFT_Y + PLAY_HEIGHT))

        # Obkreslíme finální velký rámeček kolem desky pro estetiku
        pygame.draw.rect(surface, RED, (TOP_LEFT_X, TOP_LEFT_Y, PLAY_WIDTH, PLAY_HEIGHT), 5)

class Game:
    """
    Hlavní řídící třída celé hry řešící veškerou logiku padání, čištění a skórování.
    """
    def __init__(self):
        self.board = Board(10, 20)
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()
        # Uchovává mapu zamčených pevných bloků {(X_col, Y_row) : (Color_RGB)}
        self.locked_positions = {}
        self.score = 0
        self.game_over = False

    def new_piece(self):
        """Vygenerování nového náhodného padajícího objektu doprostřed desky."""
        return Tetromino(self.board.width // 2 - 2, 0, random.choice(SHAPES))

    def convert_shape_format(self, piece):
        """
        Přečte matici symbolické reprezentace (s tečkami a nulami) 
        a vypočte reálné herní souřadnice bloků v gridech.
        """
        positions = []
        format_shape = piece.get_shape()

        for i, line in enumerate(format_shape):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    # Přidáme souřadnici platného bloku kostky (s ohledem na koordinační offset bloku)
                    positions.append((piece.x + j, piece.y + i))

        # Provedeme offset o úpravu centrální pozice matice shluků
        for i, pos in enumerate(positions):
            positions[i] = (pos[0] - 2, pos[1] - 4)

        return positions

    def valid_space(self, piece):
        """
        Ověřuje, zda je nový zamýšlený pohyb z pohledu X a Y platný.
        Nesmí narazit ani do zdi, ani do podlahy a už vůbec ne do jiné kostičky!
        """
        # Vygenerujeme všechny přípustné prázdné plochy v tuto chvíli
        accepted_pos = [[(j, i) for j in range(10) if self.board.grid[i][j] == BLACK] for i in range(20)]
        accepted_pos = [j for sub in accepted_pos for j in sub] # Konverze 2D pole na 1D array

        formatted = self.convert_shape_format(piece) # Spočítání aktuálního pohybu u této kostky

        for pos in formatted:
            if pos not in accepted_pos:
                # Bloky co se rodí úplně nahoře u stropu musíme přehlížet, tam jsou Y hodnoty záporné
                if pos[1] > -1:
                    return False
        return True

    def check_lost(self):
        """
        Zkontroluje, jestli se nám nahromaděné kostky nedotkly stropu plochy.
        """
        for pos in self.locked_positions:
            x, y = pos
            if y < 1: 
                return True
        return False

    def clear_rows(self):
        """
        Projít veškeré řádky odspodu (od 19 po 0).
        Pokud je v řádku zaplněno plných 10 míst, řádek se umaže a vše nad ním spadne o +1 dolů.
        """
        inc = 0
        for i in range(len(self.board.grid) - 1, -1, -1):
            row = self.board.grid[i]
            if BLACK not in row: # Ani jedno prázdné políčko! Odstranit celý řádek
                inc += 1
                ind = i
                # Vymazání z dictionary locked positions daného celého jednoho řádku
                for j in range(len(row)):
                    try:
                        del self.locked_positions[(j, i)]
                    except:
                        continue

        if inc > 0:
            # Shiftování objektů, co leží nad odebraným řádkem, dolů
            for key in sorted(list(self.locked_positions), key=lambda x: x[1])[::-1]:
                x, y = key
                if y < ind: # Pokud jsi výše než ten odstraněný řádek...
                    newKey = (x, y + inc) # ...připíšeme ti Y posun dolů o počet smazaných
                    self.locked_positions[newKey] = self.locked_positions.pop(key)
            
            # Navýšení skóre! (za více řádků najednou je logaritmicky lepší skóre)
            self.score += inc * 10 * inc

    def draw_text_middle(self, surface, text, size, color):
        """Pomocná funkce k psaní velkým středovým textem na palubku (např Game Over)."""
        font = pygame.font.SysFont('comicsans', size, bold=True)
        label = font.render(text, 1, color)
        # Zarovná text přesně doprostřed podle jeho vlastních rozměrů textu
        surface.blit(label, (TOP_LEFT_X + PLAY_WIDTH/2 - (label.get_width() / 2), TOP_LEFT_Y + PLAY_HEIGHT/2 - label.get_height()/2))

    def draw(self, surface):
        """
        Hlavní vykreslovací smyčka logiky pro vygenerování jednoho vizuálního políčka na monitor.
        """
        surface.fill(BLACK) # Nastavení černého malířského plátna

        pygame.font.init()
        font = pygame.font.SysFont('comicsans', 60)
        label = font.render('TETRIS', 1, WHITE)
        # Nápis hry úplně nahoře obrazovky!
        surface.blit(label, (TOP_LEFT_X + PLAY_WIDTH / 2 - (label.get_width() / 2), 30))

        font = pygame.font.SysFont('comicsans', 30)
        
        # Obarvení skóre
        score_label = font.render(f'Skóre: {self.score}', 1, WHITE)
        sx = TOP_LEFT_X + PLAY_WIDTH + 50
        sy = TOP_LEFT_Y + PLAY_HEIGHT/2 - 100
        surface.blit(score_label, (sx, sy))

        # Obrazovka pro 'Další'
        next_label = font.render('Další tvar:', 1, WHITE)
        surface.blit(next_label, (sx, sy + 160))
        # Vykreslení miniaturního náhledu do prava vedle gridu pro Další kus
        format_shape = self.next_piece.shape[self.next_piece.rotation % len(self.next_piece.shape)]
        for i, line in enumerate(format_shape):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    pygame.draw.rect(surface, self.next_piece.color, (sx + j*BLOCK_SIZE, sy + 200 + i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

        # Volání Board pro dokreslení samotných zamčených bloků
        self.board.grid = self.board.create_grid(self.locked_positions)
        self.board.draw(surface)

        # A nakonec letící plynulá kostička!
        piece_pos = self.convert_shape_format(self.current_piece)
        for i in range(len(piece_pos)):
            x, y = piece_pos[i]
            # Kreslíme jej jen tehdy, pokud aspoň polovičním tělem vlítla již do místnosti (Y se stalo > -1)
            if y > -1:
                pygame.draw.rect(surface, self.current_piece.color, (TOP_LEFT_X + x * BLOCK_SIZE, TOP_LEFT_Y + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

        pygame.display.update()

def main():
    """Startovní a inicializační funkce, řídící pygame cyklus, klávesy atd."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Tetris - Fáze 2')
    
    game = Game()
    clock = pygame.time.Clock()
    
    fall_time = 0     # Počítadlo času k dopadající logice (měřeno v milisekundách)
    fall_speed = 0.27 # Jak rychle to spadne o patro dolů (v sekundách)
    
    run = True
    while run:
        # Pokaždé obnovíme plochu podle napadaných pevných bloků z minula
        game.board.grid = game.board.create_grid(game.locked_positions)
        
        fall_time += clock.get_rawtime()
        clock.tick() 

        # Logika padání podle nastaveného času (fall_speed)
        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            game.current_piece.y += 1
            # Když ten pád způsobí, že narazím... to značí konec naší svobody pohybu pro danou kostku (uzamčení zespodu)
            if not (game.valid_space(game.current_piece)) and game.current_piece.y > 0:
                game.current_piece.y -= 1
                change_piece = True
            else:
                change_piece = False

        # Odposlouchávač pro PyGame akce a klávesnice!
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT: # Chci Doleva
                    game.current_piece.x -= 1
                    if not game.valid_space(game.current_piece): # Jsem naletěl do již položené kostky, nebo zdi? Zpátky!
                        game.current_piece.x += 1
                elif event.key == pygame.K_RIGHT: # Chci Doprava
                    game.current_piece.x += 1
                    if not game.valid_space(game.current_piece): 
                        game.current_piece.x -= 1
                elif event.key == pygame.K_DOWN: # Chci pohnout dolů zrychleně
                    game.current_piece.y += 1
                    if not game.valid_space(game.current_piece):
                        game.current_piece.y -= 1
                elif event.key == pygame.K_UP: # Rotování ve směru hodinových map
                    game.current_piece.rotation += 1
                    if not game.valid_space(game.current_piece): # Pokud mi rotace přetne okraj zdi, rotuj se prosím zpátky
                        game.current_piece.rotation -= 1

        piece_pos = game.convert_shape_format(game.current_piece)
        
        # Kontrola stvrzujícího uzamčení plošinky
        if 'change_piece' in locals() and change_piece:
            for pos in piece_pos:
                p = (pos[0], pos[1])
                # Uložení trvale zbarveného stávajícího kvádru do herního slovníku
                game.locked_positions[p] = game.current_piece.color
            
            game.current_piece = game.next_piece
            game.next_piece = game.new_piece()
            change_piece = False
            
            # Smažeme kompletní řady napadané pro toto herní kolo
            game.clear_rows()

        game.draw(screen)

        # Detekce konce hry (napříč ohraničení Y - prohra)
        if game.check_lost():
            game.draw_text_middle(screen, "Game Over", 80, WHITE)
            pygame.display.update()
            pygame.time.delay(1500) # Dej hráči delší prodlevu pro spatření konce, než se okno zavře
            run = False

if __name__ == '__main__':
    main()
