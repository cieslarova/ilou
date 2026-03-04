import pygame
import time

# Inicializace hry
pygame.init()

# Barvy
CERNA = (0, 0, 0)
ruzova = (213, 50, 80)
zelena = (0, 255, 0)

# Velikost okna
sirka_okna = 600
vyska_okna = 400

# Vytvoření okna
okno = pygame.display.set_mode((sirka_okna, vyska_okna))
pygame.display.set_caption('Duhový Had - Fáze 1 (Základní pohyb)')

# Hodiny
hodiny = pygame.time.Clock()
rychlost_hada = 10
velikost_bloku = 10

def herni_smycka():
    hra_konci = False

    # Pozice hada (začíná uprostřed)
    x1 = sirka_okna / 2
    y1 = vyska_okna / 2
    x1_zmena = 0
    y1_zmena = 0

    while not hra_konci:
        for udalost in pygame.event.get():
            if udalost.type == pygame.QUIT:
                hra_konci = True
            # Ovládání pohybu
            if udalost.type == pygame.KEYDOWN:
                if udalost.key == pygame.K_LEFT:
                    x1_zmena = -velikost_bloku
                    y1_zmena = 0
                elif udalost.key == pygame.K_RIGHT:
                    x1_zmena = velikost_bloku
                    y1_zmena = 0
                elif udalost.key == pygame.K_UP:
                    y1_zmena = -velikost_bloku
                    x1_zmena = 0    
                elif udalost.key == pygame.K_DOWN:
                    y1_zmena = velikost_bloku
                    x1_zmena = 0

        # Ve fázi 1 hru ukončíme při nárazu do zdi
        if x1 >= sirka_okna or x1 < 0 or y1 >= vyska_okna or y1 < 0:
            hra_konci = True
        
        x1 += x1_zmena
        y1 += y1_zmena
        okno.fill(CERNA)
        
        # Vykreslení hada (jen jedna kostka)
        pygame.draw.rect(okno, zelena, [x1, y1, velikost_bloku, velikost_bloku])
        
        pygame.display.update()
        hodiny.tick(rychlost_hada)

    pygame.quit()
    quit()

# Spuštění hry
herni_smycka()
