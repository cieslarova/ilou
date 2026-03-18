import pygame
import random

# Inicializace herních modulů
pygame.init()

# Definice základních barev (RGB formát) pro vykreslování
CERVENA = (213, 50, 80)
MODRA_OBLOHA = (135, 206, 235)
ZELENA_TRUBA = (0, 255, 0)
ZALTA_PTAK = (255, 255, 0)
CERNA = (0, 0, 0)

# Inicializace hlavního okna hry
sirka_okna = 600
vyska_okna = 400
okno = pygame.display.set_mode((sirka_okna, vyska_okna))
pygame.display.set_caption('Flappy Pták - Fáze 2: Překážky')

# Počáteční nastavení hodnot reprezentující ptáka (pozice a pohybující síly)
ptak_x = 50.0
ptak_y = float(vyska_okna // 2)
ptak_velikost = 30
ptak_y_zmena = 0.0
gravitace = 0.8
skok = -10.0

# Počáteční hodnoty překážek (trubek)
trubka_sirka = 50
trubka_mezera = 150
trubka_x = float(sirka_okna)
# Náhodné generování výšky překážky
trubka_vyska = random.randint(50, vyska_okna - trubka_mezera - 50)
rychlost = 5.0

# Skóre a nastavení vykreslování písma
skore = 0
font = pygame.font.SysFont("bahnschrift", 25)
hodiny = pygame.time.Clock()
fps = 30

def reset_hry():
    """
    Funkce resetuje globální proměnné hry na jejich výchozí stav pro novou hru.
    Je volána po nárazu (konci hry) ve chvíli, kdy uživatel zmáčkne mezerník pro restart.
    """
    global ptak_y, ptak_y_zmena, trubka_x, trubka_vyska, skore
    ptak_y = float(vyska_okna // 2)
    ptak_y_zmena = 0.0
    trubka_x = float(sirka_okna)
    trubka_vyska = random.randint(50, vyska_okna - trubka_mezera - 50)
    skore = 0

# Stavové proměnné (běh okna a aktivní hra bez kolize)
bezi = True
hra_bezi = True

# Hlavní herní smyčka vykreslující obraz a počítající fyziku
while bezi:
    # Systém zpracování událostí odeslaných z PyGame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            bezi = False
        # Rozpoznání vstupu od uživatele pro interakci ve hře
        if event.type == pygame.KEYDOWN:
            # Reakce na zmáčknutí mezerníku nebo šipky nahoru
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                if hra_bezi:
                    # Vyslání negativního směru změny na Y osu (skok o krok nahoru)
                    ptak_y_zmena = float(skok)
                else:
                    # Restart při zmáčknutí tlačítka pro stav ukončení hry
                    reset_hry()
                    hra_bezi = True

    # Jestliže je hráč živý, řeší funkční mechanismy překážek a bodů 
    if hra_bezi:
        # Fyzika ptáka (zapojení gravitace k přitahování ptáka k zemi)
        ptak_y_zmena += gravitace
        ptak_y += ptak_y_zmena

        # Pohyb překážek proti hráči (z pohledu hráče - let zprava doleva)
        trubka_x -= rychlost
        # Pokud překážka proletí oknem odebírá se a respawnuje se vpředu s novými rozměry
        if trubka_x < -trubka_sirka:
            trubka_x = float(sirka_okna)
            trubka_vyska = random.randint(50, vyska_okna - trubka_mezera - 50)
            skore += 1

        # Definováni reálných "Hitboxů" obdélníků prvků nutných k zjištění kolizí
        ptak_rect = pygame.Rect(int(ptak_x), int(ptak_y), ptak_velikost, ptak_velikost)
        trubka_horni = pygame.Rect(int(trubka_x), 0, trubka_sirka, trubka_vyska)
        trubka_dolni = pygame.Rect(int(trubka_x), trubka_vyska + trubka_mezera, trubka_sirka, vyska_okna)

        # Matematické detekce kolizí skrze knihovní funkci (při nárazu "umře")
        if ptak_rect.colliderect(trubka_horni) or ptak_rect.colliderect(trubka_dolni):
            hra_bezi = False
        # "Umře" pokud propadne podlahou nebo zaletí do stropu
        if ptak_y < 0 or ptak_y + ptak_velikost > vyska_okna:
            hra_bezi = False
    else:
        # Inicializace rectů pro vykreslení i v "mrtvém" stavu (aby nekřičel linter
        # neboť program padl do dead-endu a pták a trubky stále čekají obdélníky na vykreslení)
        ptak_rect = pygame.Rect(int(ptak_x), int(ptak_y), ptak_velikost, ptak_velikost)
        trubka_horni = pygame.Rect(int(trubka_x), 0, trubka_sirka, trubka_vyska)
        trubka_dolni = pygame.Rect(int(trubka_x), trubka_vyska + trubka_mezera, trubka_sirka, vyska_okna)

    # Rendering: Grafika překreslování po změně matematických hodnot výše v kódu
    okno.fill(MODRA_OBLOHA)
    
    # Trubky
    pygame.draw.rect(okno, ZELENA_TRUBA, trubka_horni)
    pygame.draw.rect(okno, ZELENA_TRUBA, trubka_dolni)
    
    # Pták
    pygame.draw.rect(okno, ZALTA_PTAK, ptak_rect)

    # Skóre
    img_skore = font.render(f"Skóre: {skore}", True, CERNA)
    okno.blit(img_skore, (10, 10))

    # Konec hry alert info na ploše
    if not hra_bezi:
        stop_text = font.render("Konec! Mezerník pro restart", True, CERVENA)
        okno.blit(stop_text, (sirka_okna // 2 - 100, vyska_okna // 2))

    # Přesun frame do obrazovky pro PyGame okno a 30 FPS tick
    pygame.display.update()
    hodiny.tick(fps)

# Uzavření aplikace
pygame.quit()
