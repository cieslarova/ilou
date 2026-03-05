import pygame
import time
import random

# Inicializace hry
pygame.init()

# Barvy
CERNA = (0, 0, 0)
BILA = (255, 255, 255)
ruzova = (213, 50, 80)
modra = (50, 153, 213)
zluta = (255, 255, 102)
zelena = (0, 255, 0)
fialova = (128, 0, 128)
oranzova = (255, 165, 0)

barvy_jidla = [ruzova, modra, zluta, zelena, fialova, oranzova]

# Velikost okna
sirka_okna = 600
vyska_okna = 400

# Vytvoření okna
okno = pygame.display.set_mode((sirka_okna, vyska_okna))
pygame.display.set_caption('Duhový Had - Fáze 2 (Jídlo, růst a obtočení)')

# Hodiny
hodiny = pygame.time.Clock()
rychlost_hada = 10
velikost_bloku = 10

# Font pro skóre a zprávy
font_skore = pygame.font.SysFont("bahnschrift", 25)

def zobraz_skore(skore):
    """Vykreslí aktuální skóre do levého horního rohu obrazovky."""
    hodnota = font_skore.render("Skóre: " + str(skore), True, BILA)
    okno.blit(hodnota, [0, 0])

def vykresli_hada(velikost_bloku, seznam_hada, barvy_hada):
    """
    Vykreslí celé tělo hada na obrazovku na základě uložených souřadnic.
    Každému bloku těla přiřadí barvu ze seznamu barev. Pokud nová barva
    v seznamu ještě neexistuje, náhodně ji vygeneruje (pro efekt duhového hada).
    """
    for i, x_y in enumerate(seznam_hada):
        # Generování barvy pokud v seznamu zatím pro daný článek chybí
        while len(barvy_hada) <= i:
            barvy_hada.append((random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)))
        pygame.draw.rect(okno, barvy_hada[i], [x_y[0], x_y[1], velikost_bloku, velikost_bloku])

def herni_smycka():
    """
    Hlavní smyčka hry, která řídí celý program.
    Zpracovává stisky kláves, aktualizuje souřadnice hlavy, 
    kontroluje události (jídlo, obtočení, náraz do těla)
    a stará se o opakované překreslování okna.
    """
    hra_konci = False
    hra_zavrena = False

    # Pozice hada
    x1 = sirka_okna / 2
    y1 = vyska_okna / 2
    x1_zmena = 0
    y1_zmena = 0

    # Tělo hada
    seznam_hada = []
    delka_hada = 1
    barvy_hada = []

    # Jídlo
    jidlo_x = round(random.randrange(0, sirka_okna - velikost_bloku) / 10.0) * 10.0
    jidlo_y = round(random.randrange(0, vyska_okna - velikost_bloku) / 10.0) * 10.0
    barva_jidla = random.choice(barvy_jidla)

    while not hra_konci:
        while hra_zavrena:
            okno.fill(CERNA)
            zprava = font_skore.render("Konec hry! Q-Konec nebo R-Znovu", True, ruzova)
            okno.blit(zprava, [sirka_okna / 6, vyska_okna / 3])
            skore = delka_hada - 1
            zobraz_skore(skore)
            pygame.display.update()

            for udalost in pygame.event.get():
                if udalost.type == pygame.QUIT:
                    hra_konci = True
                    hra_zavrena = False
                if udalost.type == pygame.KEYDOWN:
                    if udalost.key == pygame.K_q:
                        hra_konci = True
                        hra_zavrena = False
                    if udalost.key == pygame.K_r:
                        herni_smycka()
                        return

        for udalost in pygame.event.get():
            if udalost.type == pygame.QUIT:
                hra_konci = True
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

        # Logika pro obtočení obrazovky ("průjezd zdí"):
        # Pokud hlava hada přejede za pravý (širší) nebo levý (užší) okraj,
        # změní souřadnici tak, aby ze strany protilehlé "vyjela".
        if x1 >= sirka_okna:
            x1 = 0
        elif x1 < 0:
            x1 = sirka_okna - velikost_bloku

        if y1 >= vyska_okna:
            y1 = 0
        elif y1 < 0:
            y1 = vyska_okna - velikost_bloku
        
        x1 += x1_zmena
        y1 += y1_zmena
        okno.fill(CERNA)
        
        # Vykreslení jídla
        pygame.draw.rect(okno, barva_jidla, [jidlo_x, jidlo_y, velikost_bloku, velikost_bloku])
        
        # Udržování správné délky hada:
        # Pokaždé přidáme novou pozici (hlava_hada) na konec jeho těla (seznam_hada).
        # Pokud je v seznamu uloženo více bloků než jaká je aktuální délka hada,
        # smažeme vždy ten první (nejstarší) blok, tedy konec (ocas) hada. Bylo by jich moc.
        hlava_hada = [x1, y1]
        seznam_hada.append(hlava_hada)
        
        if len(seznam_hada) > delka_hada:
            del seznam_hada[0]

        # Kontrola nárazu do vlastního těla 
        for x in seznam_hada[:-1]:
            if x == hlava_hada:
                hra_zavrena = True

        vykresli_hada(velikost_bloku, seznam_hada, barvy_hada)

        # Skóre
        skore = delka_hada - 1
        zobraz_skore(skore)

        pygame.display.update()

        # Detekce snědení jídla a prodlužování hada:
        # Porovnání souřadnic. Pokud se obě osy (X a Y) rovnají souřadnicím jídla,
        # vygenerujeme na náhodné pozici jídlo nové, zvětšíme globální délku hada
        # a přidáme zároveň náhodnou barvu do seznamu pro nový blok.
        if x1 == jidlo_x and y1 == jidlo_y:
            jidlo_x = round(random.randrange(0, sirka_okna - velikost_bloku) / 10.0) * 10.0
            jidlo_y = round(random.randrange(0, vyska_okna - velikost_bloku) / 10.0) * 10.0
            delka_hada += 1
            barvy_hada.append((random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)))
            barva_jidla = random.choice(barvy_jidla)

        hodiny.tick(rychlost_hada)

    pygame.quit()
    quit()

# Spuštění hry
herni_smycka()
