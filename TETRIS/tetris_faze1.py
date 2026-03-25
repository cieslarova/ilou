import pygame
import random

# --- Konstanty pro hru ---
# Rozměry obrazovky
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
PLAY_WIDTH = 300  # 10 * 30 pixelů
PLAY_HEIGHT = 600  # 20 * 30 pixelů
BLOCK_SIZE = 30

# Pozice levého horního rohu hrací plochy
TOP_LEFT_X = (SCREEN_WIDTH - PLAY_WIDTH) // 2
TOP_LEFT_Y = SCREEN_HEIGHT - PLAY_HEIGHT - 50

# Barvy
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
# Každý tvar je definován jako seznam 5x5 matic, kde každá matice představuje jednu rotaci.
# '0' znamená blok, '.' znamená prázdné místo.

S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '...0.',
      '..00.',
      '..0..',
      '.....']]

I = [['.....',
      '..0..',
      '..0..',
      '..0..',
      '..0..'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

# Seznam všech tvarů a jejich barev
SHAPES = [S, Z, I, O, J, L, T]
SHAPE_COLORS = [GREEN, RED, CYAN, YELLOW, ORANGE, BLUE, PURPLE]


# --- Třída Tetromino ---
class Tetromino:
    """
    Reprezentuje jeden padající blok (tetromino) ve hře.
    Obsahuje informace o tvaru, barvě, pozici a rotaci.
    """

    def __init__(self, x, y, shape):
        """
        Inicializuje nové tetromino.
        :param x: Počáteční X souřadnice (sloupec na herní desce).
        :param y: Počáteční Y souřadnice (řádek na herní desce).
        :param shape: Seznam matic definujících tvar a jeho rotace.
        """
        self.x = x
        self.y = y
        self.shape = shape
        self.color = SHAPE_COLORS[SHAPES.index(shape)]  # Přiřadí barvu podle indexu tvaru
        self.rotation = 0  # Aktuální rotace (index v seznamu tvarů)

    def get_shape(self):
        """
        Vrátí aktuální tvar tetromina na základě jeho rotace.
        :return: Matice 5x5 reprezentující aktuální tvar.
        """
        return self.shape[self.rotation % len(self.shape)]


# --- Třída Board ---
class Board:
    """
    Reprezentuje herní desku Tetrisu.
    Spravuje stav mřížky (grid), kde jsou uloženy zamčené bloky.
    """

    def __init__(self, width, height):
        """
        Inicializuje herní desku.
        :param width: Šířka desky v blocích.
        :param height: Výška desky v blocích.
        """
        self.width = width
        self.height = height
        self.grid = self.create_grid()  # Vytvoří prázdnou mřížku

    def create_grid(self):
        """
        Vytvoří a vrátí prázdnou herní mřížku.
        Každá buňka je inicializována na černou barvu (prázdná).
        :return: 2D seznam reprezentující herní mřížku.
        """
        # Mřížka je seznam seznamů, kde každý vnitřní seznam je řádek.
        # Každý prvek vnitřního seznamu je barva bloku (nebo BLACK pro prázdné místo).
        grid = [[BLACK for _ in range(self.width)] for _ in range(self.height)]
        return grid

    def draw(self, surface):
        """
        Vykreslí herní desku na danou Pygame plochu.
        Vykreslí mřížku a všechny zamčené bloky.
        :param surface: Pygame plocha, na kterou se má kreslit.
        """
        # Vykreslení mřížky (čáry)
        for i in range(self.height):
            for j in range(self.width):
                # Vykreslí obdélník pro každý blok na základě barvy v mřížce
                pygame.draw.rect(surface, self.grid[i][j],
                                 (TOP_LEFT_X + j * BLOCK_SIZE, TOP_LEFT_Y + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

        # Vykreslení ohraničení hrací plochy
        pygame.draw.rect(surface, WHITE, (TOP_LEFT_X, TOP_LEFT_Y, PLAY_WIDTH, PLAY_HEIGHT), 4)


# --- Třída Game ---
class Game:
    """
    Hlavní třída pro správu herního stavu a logiky.
    """

    def __init__(self):
        """
        Inicializuje herní instanci.
        """
        self.board = Board(10, 20)  # Vytvoří herní desku 10x20 bloků
        self.current_piece = self.new_piece()  # Aktuálně padající blok
        self.next_piece = self.new_piece()  # Další blok v pořadí
        self.score = 0  # Skóre hráče
        self.game_over = False  # Příznak konce hry

    def new_piece(self):
        """
        Generuje nový náhodný tetromino a vrací ho.
        :return: Nová instance Tetromino.
        """
        # Nový blok se objeví nahoře uprostřed herní desky.
        return Tetromino(self.board.width // 2 - 2, 0, random.choice(SHAPES))

    def draw(self, surface):
        """
        Vykreslí všechny herní prvky na danou Pygame plochu.
        Zahrnuje desku, aktuální blok, skóre a další informace.
        :param surface: Pygame plocha, na kterou se má kreslit.
        """
        # Vyplní pozadí obrazovky černou barvou
        surface.fill(BLACK)

        # Vykreslí herní desku
        self.board.draw(surface)

        # Vykreslí aktuální padající blok
        # Prochází matici tvaru bloku
        format_shape = self.current_piece.get_shape()
        for i, line in enumerate(format_shape):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':  # Pokud je to část bloku
                    # Vypočítá skutečné souřadnice na obrazovce
                    x = TOP_LEFT_X + (self.current_piece.x + j) * BLOCK_SIZE
                    y = TOP_LEFT_Y + (self.current_piece.y + i) * BLOCK_SIZE
                    # Vykreslí blok s jeho barvou
                    pygame.draw.rect(surface, self.current_piece.color, (x, y, BLOCK_SIZE, BLOCK_SIZE), 0)

        # Zobrazí skóre (zatím jen placeholder)
        font = pygame.font.SysFont('comicsans', 30)
        label = font.render(f'Skóre: {self.score}', 1, WHITE)
        surface.blit(label, (TOP_LEFT_X + PLAY_WIDTH + 50, TOP_LEFT_Y + 100))

        # Zobrazí "další blok" (zatím jen placeholder)
        label = font.render('Další:', 1, WHITE)
        surface.blit(label, (TOP_LEFT_X - 150, TOP_LEFT_Y + 100))

        # Aktualizuje celou obrazovku
        pygame.display.update()


# --- Hlavní herní smyčka ---
def main():
    """
    Hlavní funkce, která inicializuje Pygame a spouští herní smyčku.
    """
    pygame.init()  # Inicializace Pygame
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Nastavení velikosti okna
    pygame.display.set_caption('Tetris - Fáze 1')  # Nastavení titulku okna

    game = Game()  # Vytvoření instance hry
    clock = pygame.time.Clock()  # Pro řízení snímkové frekvence

    run = True
    while run:
        # Omezení snímkové frekvence na 60 FPS
        clock.tick(60)

        # Zpracování událostí
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Pokud uživatel zavře okno
                run = False

        # Vykreslení herního stavu
        game.draw(screen)

    pygame.quit()  # Ukončení Pygame


if __name__ == '__main__':
    main()
