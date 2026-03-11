import pygame
import random

pygame.init()

# Barvy
ruzova = (255, 105, 180)
modra = (0, 0, 255)
BILA = (255, 255, 255)

# Velikost okna
sirka_okna = 300
vyska_okna = 300

# Vytvoření okna
okno = pygame.display.set_mode((sirka_okna, vyska_okna))
pygame.display.set_caption("Košík - Fáze 1 (Základy pohybu)")

# Hráč (Základní čtvereček dole)
hrac_x = 150
hrac_velikost = 25
hrac_rychlost = 10
hrac_y = vyska_okna - hrac_velikost

# Padající kostka
kostka_velikost = 15
kostka_rychlost = 3
kostka_x = random.randint(0, sirka_okna - kostka_velikost)
kostka_y = 0

# Hlavní herní smyčka
bezi = True
clock = pygame.time.Clock()

while bezi:
    # 1. Zpracování událostí
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            bezi = False

    # 2. Pohyb hráče
    stisknute_klavesy = pygame.key.get_pressed()
    if stisknute_klavesy[pygame.K_LEFT]:
        hrac_x -= hrac_rychlost
    if stisknute_klavesy[pygame.K_RIGHT]:
        hrac_x += hrac_rychlost

    # Omezení hráče na hrací plochu
    if hrac_x < 0:
        hrac_x = 0
    if hrac_x > sirka_okna - hrac_velikost:
        hrac_x = sirka_okna - hrac_velikost

    # 3. Pohyb padající kostky
    kostka_y += kostka_rychlost

    # Reset kostky, když překročí spodní okraj obrazovky
    if kostka_y > vyska_okna:
        kostka_y = 0
        kostka_x = random.randint(0, sirka_okna - kostka_velikost)

    # 4. Detekce kolize (hráč chytil kostku)
    if (hrac_x < kostka_x + kostka_velikost and
        hrac_x + hrac_velikost > kostka_x and
        hrac_y < kostka_y + kostka_velikost and
        hrac_y + hrac_velikost > kostka_y):
        # Kostka chycena, reset
        kostka_y = 0
        kostka_x = random.randint(0, sirka_okna - kostka_velikost)

    # 5. Vykreslování
    okno.fill(BILA) # Vymažeme předchozí snímek
    
    # Vykreslení kostky
    pygame.draw.rect(okno, modra, (kostka_x, kostka_y, kostka_velikost, kostka_velikost))
    
    # Vykreslení hráče
    pygame.draw.rect(okno, ruzova, (hrac_x, hrac_y, hrac_velikost, hrac_velikost))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
