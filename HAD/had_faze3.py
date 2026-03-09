import pygame
import time
import random
import os

# Inicializace hry a modulu pygame
pygame.init()

# Definice základních barev (RGB) pro použití ve hře
CERNA = (0, 0, 0)
BILA = (255, 255, 255)
ruzova = (213, 50, 80)
modra = (50, 153, 213)
zluta = (255, 255, 102)
zelena = (0, 255, 0)
fialova = (128, 0, 128)
oranzova = (255, 165, 0)

# Seznam barev, ze kterého se náhodně volí barva jídla
barvy_jidla = [ruzova, modra, zluta, zelena, fialova, oranzova]

# Velikost a nastavení okna hry
sirka_okna = 600
vyska_okna = 400

# Vytvoření hlavního herního okna a nastavení jeho titulku
okno = pygame.display.set_mode((sirka_okna, vyska_okna))
pygame.display.set_caption('Duhový Had - Fáze 3 (Menu, Skóre, Pauza)')

# Inicializace hodin pro kontrolu rychlosti obnovy (FPS)
hodiny = pygame.time.Clock()
rychlost_hada = 10

# Nastavení velikosti jednoho čtvercového bloku hada (v pixelech)
velikost_bloku = 10

# Nastavení fontu pro výpis aktuálního skóre
font_skore = pygame.font.SysFont("bahnschrift", 25)

# Proměnné udržující jméno hráče a seznam nejlepších skóre
jmeno_hrace = ""
high_scores = []  # Bude obsahovat seznam dvojic (jméno, skóre)
nejlepsi_skore = 0

# Načtení historie nejlepších skóre z textového souboru při startu hry
if os.path.exists("had_skore.txt"):
    try:
        # Přečteme řádky, ignorujeme prázdné
        with open("had_skore.txt", "r") as f:
            lines = [radek.strip() for radek in f.readlines() if radek.strip()]
        
        if lines:
            # Kompatibilita se starším formátem, kde bylo uloženo jen skóre (bez jména a středníku)
            if ";" not in lines[0]:
                nejlepsi_skore = int(lines[0])
                high_scores.append(("Neznámý", nejlepsi_skore))
            else:
                # Načtení formátu Jmeno;Skore pro každý řádek v souboru
                for line in lines:
                    if ";" in line:
                        jmeno, body = line.split(";", 1)
                        try:
                            # Pokus o převod získaného skóre na celé číslo
                            sk = int(body)
                            high_scores.append((jmeno, sk))
                        except ValueError:
                            # Ignorování chybného řádku
                            continue
                # Pokud se podařilo načíst skóre, určíme z nich to nejvyšší
                if high_scores:
                    nejlepsi_skore = max(sk for _, sk in high_scores)
    except Exception:
        # V případě jakékoliv chyby při čtení (soubor nelze otevřít, oprávnění atd.) vynulujeme seznam
        nejlepsi_skore = 0
        high_scores = []

def zobraz_skore(skore):
    """
    Vykreslí aktuální skóre hráče do levého horního rohu okna.
    
    Parametry:
    skore (int): Současná hodnota bodů hráče.
    """
    hodnota = font_skore.render("Skóre: " + str(skore), True, BILA)
    okno.blit(hodnota, [0, 0])

def vykresli_hada(velikost_bloku, seznam_hada, barvy_hada):
    """
    Vykreslí tělo hada na základě souřadnic jednotlivých článků.
    Pokud chybí barva pro článek (protože had právě vyrostl), přiřadí se náhodná barva.
    
    Parametry:
    velikost_bloku (int): Rozměr jednoho tělního bloku.
    seznam_hada (list): Souřadnice [x, y] pro každý článek hada.
    barvy_hada (list): Seznam barev, z nichž každá odpovídá jednomu článku těla.
    """
    for i, x_y in enumerate(seznam_hada):
        # Doplnění nové barvy pro nově nabyté články hada
        while len(barvy_hada) <= i:
            barvy_hada.append((random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)))
        
        # Vykreslení konkrétního článku těla hada s jeho barvou
        pygame.draw.rect(okno, barvy_hada[i], [x_y[0], x_y[1], velikost_bloku, velikost_bloku])

def zobraz_nejlepsi_skore(nejlepsi):
    """
    Zobrazí hodnotu historicky nejlepšího dosaženého skóre (rekordu) v pravém horním rohu.
    
    Parametry:
    nejlepsi (int): Nejvyšší skóre.
    """
    font_male = pygame.font.SysFont("bahnschrift", 15)
    hodnota = font_male.render("Rekord: " + str(nejlepsi), True, BILA)
    okno.blit(hodnota, [sirka_okna - 120, 0])

def zobraz_menu(nejlepsi_skore, jmeno_hrace, high_scores):
    """
    Zobrazí uvítací menu, instrukce, zadávání jména a aktuálně nejlepší hráče (Top 3).
    Tato funkce se volá při startu před vstupem do samotné herní smyčky.
    """
    okno.fill(zelena)
    
    # Renderování hlavního nadpisu hry
    font_nadpis = pygame.font.SysFont("bahnschrift", 50)
    nadpis = font_nadpis.render("Duhový Had", True, ruzova)
    nadpis_rect = nadpis.get_rect(center=(sirka_okna/2, vyska_okna/5))
    okno.blit(nadpis, nadpis_rect)

    font_menu = pygame.font.SysFont("bahnschrift", 25)

    # Vykreslení sekce pro celkový rekord a aktuálně zadávané jméno
    text_rekord = font_menu.render("Rekord: " + str(nejlepsi_skore), True, CERNA)
    okno.blit(text_rekord, (sirka_okna - 260, 80))

    if jmeno_hrace:
        zobrazene_jmeno = jmeno_hrace
    else:
        zobrazene_jmeno = "(napiš své jméno)"
    text_jmeno = font_menu.render("Jméno: " + zobrazene_jmeno, True, CERNA)
    okno.blit(text_jmeno, (sirka_okna - 260, 120))

    # Instrukce k ovládání hry
    instrukce0 = font_menu.render("Enter = spustit hru", True, CERNA)
    instrukce = font_menu.render("Mezerník = pauza", True, CERNA)
    instrukce2 = font_menu.render("Šipky = pohyb, nesmíte narazit do těla hada", True, CERNA)
    instrukce3 = font_menu.render("R = restart po skončení hry", True, CERNA)
    instrukce4 = font_menu.render("Q = konec hry", True, CERNA)
    
    okno.blit(instrukce0, (20, 140))
    okno.blit(instrukce,  (20, 170))
    okno.blit(instrukce2, (20, 200))
    okno.blit(instrukce3, (20, 230))
    okno.blit(instrukce4, (20, 260))
    
    # Seřazení hráčů podle skóre (sestupně) a vybrání nejlepších tří
    top3 = sorted(high_scores, key=lambda t: t[1], reverse=True)[:3]
    y_start = vyska_okna - 100
    
    # Výpis žebříčku hráčů, pokud již existují uložená data
    if top3:
        titulek = font_menu.render("Nejlepší hráči:", True, CERNA)
        okno.blit(titulek, (20, y_start))
        for idx, (jmeno, sk) in enumerate(top3, start=1):
            radek = font_menu.render(f"{idx}. {jmeno}: {sk}", True, CERNA)
            okno.blit(radek, (40, y_start + 30 * idx))

    pygame.display.update()

def pauza():
    """
    Zastaví běh hry a vypíše nápis 'Pauza'. Naslouchá klávesám pro pokračování nebo ukončení.
    """
    pauza_aktivni = True
    while pauza_aktivni:
        font_pauza = pygame.font.SysFont("bahnschrift", 25)
        zprava = font_pauza.render("Pauza", True, BILA)
        text_rect = zprava.get_rect(center=(sirka_okna/2, vyska_okna/2))
        okno.blit(zprava, text_rect)
        pygame.display.update() 

        # Čekání na vstup od uživatele pro odpausování (Mezerník) nebo ukončení (Q)
        for udalost in pygame.event.get():
            if udalost.type == pygame.QUIT:
                pygame.quit()
                quit()
            if udalost.type == pygame.KEYDOWN:
                if udalost.key == pygame.K_SPACE:
                    pauza_aktivni = False
                if udalost.key == pygame.K_q:
                    pygame.quit()
                    quit()

def herni_smycka():
    """
    Hlavní herní smyčka obsluhující běh samotné hry od prvního pohybu hada až po Game Over obrazovku.
    """
    global nejlepsi_skore, high_scores, jmeno_hrace

    hra_konci = False
    hra_zavrena = False

    # Startovní pozice hada (uprostřed okna)
    x1 = sirka_okna / 2
    y1 = vyska_okna / 2
    
    # Počáteční rychlost změny - had stojí
    x1_zmena = 0
    y1_zmena = 0

    # Inicializace seznamu jednotlivých bloků reprezentujících tělo hada
    seznam_hada = []
    delka_hada = 1
    barvy_hada = []

    # Náhodné generování původní pozice a barvy jídla (počítáno v násobcích velikosti bloku)
    jidlo_x = round(random.randrange(0, sirka_okna - velikost_bloku) / 10.0) * 10.0
    jidlo_y = round(random.randrange(0, vyska_okna - velikost_bloku) / 10.0) * 10.0
    barva_jidla = random.choice(barvy_jidla)

    while not hra_konci:
        # Fáze "Game Over" – po nabourání do sebe
        while hra_zavrena:
            okno.fill(CERNA)
            zprava = font_skore.render("Konec hry! Q-Konec nebo R-Znovu", True, ruzova)
            okno.blit(zprava, [sirka_okna / 6, vyska_okna / 3])
            
            # Skóre se rovná počtu snědených jídel (délka - 1)
            skore = delka_hada - 1
            zobraz_skore(skore)
            zobraz_nejlepsi_skore(nejlepsi_skore)
            pygame.display.update()

            # Zpracování kláves po smrti hada
            for udalost in pygame.event.get():
                if udalost.type == pygame.QUIT:
                    hra_konci = True
                    hra_zavrena = False
                if udalost.type == pygame.KEYDOWN:
                    if udalost.key == pygame.K_q:
                        hra_konci = True
                        hra_zavrena = False
                    if udalost.key == pygame.K_r:
                        # Rekurzivní restart smyčky
                        herni_smycka()
                        return

        # Fáze běhu aktuální herní smyčky - zpracování vstupu
        for udalost in pygame.event.get():
            if udalost.type == pygame.QUIT:
                hra_konci = True
            if udalost.type == pygame.KEYDOWN:
                # Pohyb podle stisknutých šipek (ošetření logiky pro jednotlivé směry)
                if udalost.key == pygame.K_SPACE:
                    pauza()
                elif udalost.key == pygame.K_LEFT:
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

        # Logika pro "procházení stěnami" – překážky nejsou hrany okna
        if x1 >= sirka_okna:
            x1 = 0
        elif x1 < 0:
            x1 = sirka_okna - velikost_bloku

        if y1 >= vyska_okna:
            y1 = 0
        elif y1 < 0:
            y1 = vyska_okna - velikost_bloku
        
        # Aplikace pozměněného směru a souřadnic
        x1 += x1_zmena
        y1 += y1_zmena
        okno.fill(CERNA)
        
        # Vykreslení nového jídla v herním okénku
        pygame.draw.rect(okno, barva_jidla, [jidlo_x, jidlo_y, velikost_bloku, velikost_bloku])
        
        # Přidání nového prvku (hlavy) na začátek těla
        hlava_hada = [x1, y1]
        seznam_hada.append(hlava_hada)
        
        # Ořezávání těla – odstraníme ocas z předchozího kroku, pokud had právě nejí jídlo
        if len(seznam_hada) > delka_hada:
            del seznam_hada[0]

        # Kontrola, zda had nenaboural sám do sebe (iteruje přes celé tělo až k předposlednímu bloku)
        for x in seznam_hada[:-1]:
            if x == hlava_hada:
                hra_zavrena = True

        vykresli_hada(velikost_bloku, seznam_hada, barvy_hada)

        # Výpočet a uložení nejlepšího skóre po posunu
        skore = delka_hada - 1
        if skore > nejlepsi_skore:
            nejlepsi_skore = skore
            jmeno = jmeno_hrace if jmeno_hrace else "Hráč"
            
            # Připojíme do seznamu k dalšímu řazení, po seřazení uložíme do TXT
            high_scores.append((jmeno, skore))
            high_scores = sorted(high_scores, key=lambda t: t[1], reverse=True)[:3]
            try:
                # Otevření pro zápis aktualizuje tabulku permanentně
                with open("had_skore.txt", "w") as f:
                    for j, sk in high_scores:
                        f.write(f"{j};{sk}\n")
            except Exception:
                pass

        # Vykreslení aktuálního a nejlepšího dostupného skóre
        zobraz_skore(skore)
        zobraz_nejlepsi_skore(nejlepsi_skore)

        # Aktulizace celého okna na závěr běhu této smyčky
        pygame.display.update()

        # Detekce sežrání jídla, nastavení nové náhodné pozice a barev
        if x1 == jidlo_x and y1 == jidlo_y:
            jidlo_x = round(random.randrange(0, sirka_okna - velikost_bloku) / 10.0) * 10.0
            jidlo_y = round(random.randrange(0, vyska_okna - velikost_bloku) / 10.0) * 10.0
            delka_hada += 1
            # Vygenerování nové barvy pro nově přirůstající část těla
            barvy_hada.append((random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)))
            barva_jidla = random.choice(barvy_jidla)

        # Časový krok pro regulaci rychlosti hada
        hodiny.tick(rychlost_hada)

    # Čisté korektní ukončení z pygame po dojetí celého kódu
    pygame.quit()
    quit()


# Začátek vykonávání skriptu - příprava prostředí
cekam = True

# Fáze menu před samotnou hrou čekající na vstup uživatele (jmého a odklepnutí)
while cekam:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            pygame.quit()
            quit()
        if udalost.type == pygame.KEYDOWN:
            if udalost.key == pygame.K_RETURN:  
                # Vstup do hry po potvrzení
                cekam = False
            elif udalost.key == pygame.K_q:     
                # Okamžité ukončení i bez startu
                pygame.quit()
                quit()
            elif udalost.key == pygame.K_BACKSPACE:
                # Smazání znaku z vyplněného jména uživatelem
                jmeno_hrace = jmeno_hrace[:-1]
            else:
                # Logika pro sběr znaků psaných do jména hráče (omezeno na 10 písmen)
                znak = pygame.key.name(udalost.key)
                if len(znak) == 1 and len(jmeno_hrace) < 10:
                    jmeno_hrace += znak.upper()

    zobraz_menu(nejlepsi_skore, jmeno_hrace, high_scores)
    # Kontrola zobrazení menu na 60 FPS
    hodiny.tick(60)

# Potvrzení stisknutím klávesy Enter spustí hlavní smyčku hry
herni_smycka()
