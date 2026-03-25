import pygame
import random
import sys

# --- Konstanty pro hru ---
# Rozměry herní plochy v počtu bloků
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
# Velikost jedné buňky (bloku) v pixelech
CELL_SIZE = 30
# Rozměry okna Pygame
WINDOW_WIDTH = BOARD_WIDTH * CELL_SIZE + 200  # Šířka pro hru + postranní panel
WINDOW_HEIGHT = BOARD_HEIGHT * CELL_SIZE

# Barvy (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

# Barvy pro jednotlivá tetromina (pro lepší vizualizaci)
TETROMINO_COLORS = [
    CYAN,    # I
    BLUE,    # J
    ORANGE,  # L
    YELLOW,  # O
    GREEN,   # S
    PURPLE,  # T
    RED      # Z
]

# Tvary tetromin (reprezentace jako seznam souřadnic bloků relativně k pivotu)
# Každý tvar má definovány své rotační stavy.
# Pivot je obvykle [1,1] nebo [2,2] v rámci 4x4 mřížky, zde je to implicitní.
# Pro jednoduchost jsou tvary definovány jako seznamy relativních souřadnic.
# Např. [[0,0], [1,0], [2,0], [3,0]] pro 'I' tvar v horizontální orientaci.
SHAPES = {
    'I': [
        [[0, 0], [1, 0], [2, 0], [3, 0]],  # Horizontální
        [[1, 0], [1, 1], [1, 2], [1, 3]]   # Vertikální
    ],
    'J': [
        [[0, 0], [0, 1], [1, 1], [2, 1]],
        [[1, 0], [2, 0], [1, 1], [1, 2]],
        [[0, 1], [1, 1], [2, 1], [2, 2]],
        [[1, 0], [1, 1], [0, 2], [1, 2]]
    ],
    'L': [
        [[2, 0], [0, 1], [1, 1], [2, 1]],
        [[1, 0], [1, 1], [1, 2], [2, 2]],
        [[0, 0], [0, 1], [1, 1], [2, 1]],
        [[0, 0], [1, 0], [1, 1], [1, 2]]
    ],
    'O': [
        [[0, 0], [1, 0], [0, 1], [1, 1]]  # Nemá rotaci, ale pro konzistenci je zde
    ],
    'S': [
        [[1, 0], [2, 0], [0, 1], [1, 1]],
        [[0, 0], [0, 1], [1, 1], [1, 2]]
    ],
    'T': [
        [[1, 0], [0, 1], [1, 1], [2, 1]],
        [[1, 0], [0, 1], [1, 1], [1, 2]],
        [[0, 1], [1, 1], [2, 1], [1, 2]],
        [[1, 0], [1, 1], [2, 1], [1, 2]]
    ],
    'Z': [
        [[0, 0], [1, 0], [1, 1], [2, 1]],
        [[2, 0], [1, 1], [2, 1], [1, 2]]
    ]
}

# Mapování typů tetromin na jejich barvy
SHAPE_COLORS = {
    'I': TETROMINO_COLORS[0],
    'J': TETROMINO_COLORS[1],
    'L': TETROMINO_COLORS[2],
    'O': TETROMINO_COLORS[3],
    'S': TETROMINO_COLORS[4],
    'T': TETROMINO_COLORS[5],
    'Z': TETROMINO_COLORS[6]
}


class Board:
    """
    Třída reprezentující herní plochu Tetrisu.
    Spravuje stav jednotlivých buněk (prázdné/obsazené blokem) a jejich barvy.
    """
    def __init__(self, width, height):
        """
        Inicializuje herní plochu.
        :param width: Šířka plochy v počtu buněk.
        :param height: Výška plochy v počtu buněk.
        """
        self.width = width
        self.height = height
        # Herní plocha je 2D seznam, kde každá buňka obsahuje barvu bloku nebo BLACK (prázdná).
        self.grid = [[BLACK for _ in range(width)] for _ in range(height)]

    def draw(self, screen):
        """
        Vykreslí aktuální stav herní plochy na obrazovku.
        Vykresluje jak obsazené bloky, tak i mřížku pro prázdné buňky.
        :param screen: Objekt obrazovky Pygame, na který se má kreslit.
        """
        # Vykreslení obsazených bloků
        for y in range(self.height):
            for x in range(self.width):
                color = self.grid[y][x]
                if color != BLACK:  # Pokud buňka není prázdná, vykresli ji
                    pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                # Vykreslení mřížky pro všechny buňky (i prázdné)
                pygame.draw.rect(screen, GRAY, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)


class Tetromino:
    """
    Třída reprezentující jedno padající tetromino.
    Spravuje jeho tvar, barvu, pozici a rotační stav.
    """
    def __init__(self, shape_type):
        """
        Inicializuje nové tetromino.
        :param shape_type: Typ tetromina (např. 'I', 'J', 'L').
        """
        self.shape_type = shape_type
        self.color = SHAPE_COLORS[shape_type]
        self.shapes = SHAPES[shape_type]
        self.rotation_index = 0  # Aktuální rotační stav
        self.current_shape = self.shapes[self.rotation_index]
        # Počáteční pozice tetromina (horní střed herní plochy)
        self.x = BOARD_WIDTH // 2 - 2  # Posun, aby bylo zhruba uprostřed
        self.y = 0

    def get_blocks(self):
        """
        Vrátí absolutní souřadnice (x, y) všech bloků, které tvoří aktuální tetromino.
        :return: Seznam dvojic (x, y) souřadnic bloků.
        """
        blocks = []
        for dx, dy in self.current_shape:
            blocks.append((self.x + dx, self.y + dy))
        return blocks

    def draw(self, screen):
        """
        Vykreslí aktuální tetromino na obrazovku.
        :param screen: Objekt obrazovky Pygame, na který se má kreslit.
        """
        for x, y in self.get_blocks():
            pygame.draw.rect(screen, self.color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            # Přidání okraje pro lepší vizualizaci bloků
            pygame.draw.rect(screen, WHITE, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)


class Game:
    """
    Hlavní třída pro správu herního stavu a logiky Tetrisu.
    """
    def __init__(self):
        """
        Inicializuje herní komponenty a Pygame.
        """
        # Inicializace Pygame modulů
        try:
            pygame.init()
            self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
            pygame.display.set_caption("Tetris Hra")
            self.clock = pygame.time.Clock()
            self.font = pygame.font.Font(None, 36) # Základní font pro text
        except pygame.error as e:
            print(f"Chyba při inicializaci Pygame: {e}")
            sys.exit(1)

        # Vytvoření herní plochy
        self.board = Board(BOARD_WIDTH, BOARD_HEIGHT)
        self.current_tetromino = None
        self.next_tetromino = None
        self.score = 0
        self.game_over = False

        # Časování pro automatický pád tetromina
        self.fall_time = 0
        self.fall_speed = 500  # Milisekundy

    def new_tetromino(self):
        """
        Vygeneruje nové náhodné tetromino a nastaví ho jako aktuální.
        Pokud již existuje 'next_tetromino', použije ho a vygeneruje nové pro 'next_tetromino'.
        """
        if self.next_tetromino is None:
            shape_type = random.choice(list(SHAPES.keys()))
            self.current_tetromino = Tetromino(shape_type)
        else:
            self.current_tetromino = self.next_tetromino
        
        # Vygenerování dalšího tetromina pro zobrazení "next piece"
        next_shape_type = random.choice(list(SHAPES.keys()))
        self.next_tetromino = Tetromino(next_shape_type)
        # Resetování pozice next_tetromina pro zobrazení v postranním panelu
        self.next_tetromino.x = BOARD_WIDTH + 2 # Posun mimo hlavní hrací plochu
        self.next_tetromino.y = 2 # Posun dolů pro lepší viditelnost

    def run(self):
        """
        Hlavní herní smyčka.
        """
        self.new_tetromino() # Vygenerování prvního tetromina

        running = True
        while running:
            # Zpracování událostí
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                # Zde by v budoucnu byla logika pro pohyb tetromina na základě kláves.
                # Prozatím jen základní obsluha.
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            # Aktualizace herního stavu (prozatím prázdné)
            if not self.game_over:
                pass # Zde bude logika pro pád, kolize, atd.

            # Vykreslování
            self.screen.fill(BLACK) # Vyplnění pozadí černou barvou

            # Vykreslení herní plochy
            self.board.draw(self.screen)

            # Vykreslení aktuálního tetromina
            if self.current_tetromino:
                self.current_tetromino.draw(self.screen)
            
            # Vykreslení dalšího tetromina v postranním panelu
            if self.next_tetromino:
                # Zobrazení textu "NEXT"
                next_text = self.font.render("DALŠÍ:", True, WHITE)
                self.screen.blit(next_text, (BOARD_WIDTH * CELL_SIZE + 20, 20))
                # Vykreslení samotného tetromina
                self.next_tetromino.draw(self.screen)

            # Vykreslení skóre (prozatím jen placeholder)
            score_text = self.font.render(f"SKÓRE: {self.score}", True, WHITE)
            self.screen.blit(score_text, (BOARD_WIDTH * CELL_SIZE + 20, WINDOW_HEIGHT - 50))

            pygame.display.flip() # Aktualizace celé obrazovky

            # Omezení snímkové frekvence
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

# Spuštění hry
if __name__ == "__main__":
    game = Game()
    game.run()
