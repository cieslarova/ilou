import pygame
import random

pygame.init()

# Barvy
ruzova = (255, 105, 180)
BILA = (255, 255, 255)
CERNA = (0, 0, 0)
modra = (0, 0, 255)
cervena = (255, 0, 0)
zluta = (255, 255, 0)
zelena = (0, 255, 0)
fialova = (255, 0, 255)

mozne_barvy = [cervena, zluta, zelena, modra, fialova, BILA, CERNA]

# Velikost okna
sirka_okna = 300
vyska_okna = 300

okno = pygame.display.set_mode((sirka_okna, vyska_okna))
pygame.display.set_caption("Košík - Fáze 2 (Skóre a více kostek)")

font_skore = pygame.font.SysFont("bahnschrift", 25)

def zobraz_skore(skore):
    """Vykreslí aktuální skóre hráče do levého horního rohu okna."""
    hodnota = font_skore.render("Skóre: " + str(skore), True, CERNA)
    okno.blit(hodnota, [0, 0])

def zobraz_zivoty(zivoty):
    """Vykreslí aktuální počet životů hráče do pravého horního rohu okna."""
    hodnota = font_skore.render("Životy: " + str(zivoty), True, CERNA)
    okno.blit(hodnota, [sirka_okna - 120, 0])

# Hráč
hrac_x = 150
hrac_velikost = 25
hrac_rychlost = 10
hrac_y = vyska_okna - hrac_velikost

# Padající kostky
kostky = [] # Nyní máme seznam kostek, ne jen jednu
kostka_velikost = 15
kostka_rychlost = 3
kostka_interval = 1800
posledni_spawneni = pygame.time.get_ticks()

# Stav hry
skore = 0
zivoty = 5

bezi = True
clock = pygame.time.Clock()

while bezi:
    # Zpracování všech událostí ve frontě (např. zavření okna křížkem)
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            bezi = False

    # Detekce konce hry
    if zivoty <= 0:
        okno.fill((200, 200, 200)) # Zašedlé pozadí
        font_konec = pygame.font.SysFont("bahnschrift", 15)
        zprava = font_konec.render("KONEC HRY! R=Znovu, Q=Konec", True, CERNA)
        text_rect = zprava.get_rect(center=(sirka_okna/2, vyska_okna/2))
        okno.blit(zprava, text_rect)
        pygame.display.update()
        
        cekani = True
        # Smyčka čekající na akci hráče po konci hry (R pro restart, Q pro konec)
        while cekani:
            for udalost in pygame.event.get():
                if udalost.type == pygame.QUIT:
                    bezi = False
                    cekani = False
                if udalost.type == pygame.KEYDOWN:
                    if udalost.key == pygame.K_q:
                        bezi = False
                        cekani = False
                    if udalost.key == pygame.K_r:
                        # Reset hry
                        zivoty = 5
                        skore = 0
                        kostky = []
                        hrac_x = 150
                        cekani = False
        continue

    # Pohyb hráče
    stisknute_klavesy = pygame.key.get_pressed()
    if stisknute_klavesy[pygame.K_LEFT]:
        hrac_x -= hrac_rychlost
    if stisknute_klavesy[pygame.K_RIGHT]:
        hrac_x += hrac_rychlost

    if hrac_x < 0:
        hrac_x = 0
    if hrac_x > sirka_okna - hrac_velikost:
        hrac_x = sirka_okna - hrac_velikost

    # Spawnování nových kostek
    aktualni_cas = pygame.time.get_ticks()
    if aktualni_cas - posledni_spawneni >= kostka_interval:
        nova_x = random.randint(0, sirka_okna - kostka_velikost)
        nahodna_barva = random.choice(mozne_barvy)
        kostky.append([nova_x, 0, nahodna_barva]) # [x, y, barva]
        posledni_spawneni = aktualni_cas

    okno.fill((150, 200, 250)) # Světle modré pozadí

    odstranene = []
    # Zpracování každé kostky (pohyb, kolize). Používá se enumerate pro přístup k indexům.
    for i, kostka in enumerate(kostky):
        kostka[1] += kostka_rychlost

        # Vykreslení kostky
        pygame.draw.rect(okno, kostka[2], (kostka[0], kostka[1], kostka_velikost, kostka_velikost))

        # Detekce kolize s hráčem
        if (hrac_x < kostka[0] + kostka_velikost and
            hrac_x + hrac_velikost > kostka[0] and
            hrac_y < kostka[1] + kostka_velikost and
            hrac_y + hrac_velikost > kostka[1]):
            
            if i in odstranene: continue
            odstranene.append(i)
            
            # Pokud chytíme černou, ztratíme život. Jinak získáme bod.
            if kostka[2] == CERNA:
                zivoty -= 1
            else:
                skore += 1
            continue

        # Pokud kostka propadne dolů
        if kostka[1] > vyska_okna - kostka_velikost:
            if i in odstranene: continue
            odstranene.append(i)
            # Pokud propadne jinak zbarvená než černá, ztratíme život.
            if kostka[2] != CERNA:
                zivoty -= 1
            continue

    # Bezpečné odstranění kostek pomocí procházení odzadu
    # Odebíráme od konce, aby se nezměnily indexy dřívějších prvků.
    for i in sorted(odstranene, reverse=True):
        del kostky[i]

    # Vykreslení hráče
    pygame.draw.rect(okno, ruzova, (hrac_x, hrac_y, hrac_velikost, hrac_velikost))
    zobraz_skore(skore)
    zobraz_zivoty(zivoty)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
