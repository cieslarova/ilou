import pygame
import random
import os

# -------------------------------------------------------------------
# Barvy a konstanty
# -------------------------------------------------------------------
CERNA = (0, 0, 0)
BILA = (255, 255, 255)
MODRA_OBLOHA = (135, 206, 235)
ZELENA_TRUBA = (0, 255, 0)
ZALTA_PTAK = (255, 255, 0)
CERVENA = (213, 50, 80)

# Velikost okna herní plochy
SIRKA_OKNA = 600
VYSKA_OKNA = 400

# Nastavení hry
FPS = 30
SKORE_SOUBOR = "flappy_skore.txt"

# -------------------------------------------------------------------
# Funkce pro práci se soubory (High Score)
# -------------------------------------------------------------------
def nacti_skore(soubor):
    """
    Načte top 3 uložena skóre ze souboru pomocí bloku try-except.
    Vrací list n-tic (jméno, skóre) a hodnotu absolutně nejlepšího skóre.
    """
    high_scores = []
    nejlepsi_skore = 0
    # Modul OS slouží k bezpečnému zjištění existence souboru před jeho otevřením
    if os.path.exists(soubor):
        try:
            with open(soubor, "r", encoding="utf-8") as f:
                for line in f:
                    if ";" in line:
                        jmeno, body = line.strip().split(";")
                        high_scores.append((jmeno, int(body)))
            # Pokud se podařilo načíst nějaká data, zjistí nejvyšší hodnotu pro rekord
            if high_scores:
                nejlepsi_skore = max(sk for _, sk in high_scores)
        except (IOError, ValueError):
            # Pokud soubor nelze číst nebo je v něm chybný int formát
            pass
    return high_scores, nejlepsi_skore

def uloz_skore(nova_hra_jmeno, uahrane_skore):
    """
    Aplikuje aktuální skóre z právě proběhlé hry do žebříčku, pokud je dost vysoké.
    Uloží ho bezpečně na disk pro budoucí spuštění hry.
    """
    global high_scores, nejlepsi_skore
    jmeno = nova_hra_jmeno if nova_hra_jmeno else "Hráč"
    
    nalezeno = False
    # Iterujeme přes aktuální tabulku hráčů a hledáme, zda už hráč má zápis
    for i, (j, s) in enumerate(high_scores):
        if j == jmeno:
            # Pokud má historicky lepší skóre, přepíšeme ho
            if uahrane_skore > s:
                high_scores[i] = (jmeno, uahrane_skore)
            nalezeno = True
            break
            
    # Pokud jde o úplně nového hráče, zapíšeme rovnou do nového tuple v listu
    if not nalezeno:
        high_scores.append((jmeno, uahrane_skore))
        
    # Seřazení celého pole od největšího zisku po nejmenší pomocí lambda funkce a říznutí top 3 [:3]
    high_scores = sorted(high_scores, key=lambda t: t[1], reverse=True)[:3]
    if high_scores:
        nejlepsi_skore = high_scores[0][1]
        
    try:
        # Přeuložení top 3 záznamů fyzicky na disk ve strukturovaném tvaru 'Jméno;Body'
        with open(SKORE_SOUBOR, "w", encoding="utf-8") as f:
            for j, s in high_scores: 
                f.write(f"{j};{s}\n")
    except IOError:
        pass # Ignoruje případy, kdy script například nemá právo k zápisu

# -------------------------------------------------------------------
# Renderovací pomocné funkce herní zobrazení
# -------------------------------------------------------------------
def zobraz_skore(okno, font, skore):
    """ Vykreslí aktuální počet nasbíraných bodů (trubek) """
    hodnota = font.render(f"Skóre: {skore}", True, CERNA)
    okno.blit(hodnota, [10, 10])

def zobraz_nejlepsi_skore(okno, font, nejlepsi):
    """ Vykreslí tabulkový rekord jako motivaci v horním pravém rohu """
    hodnota = font.render(f"Rekord: {nejlepsi}", True, CERNA)
    okno.blit(hodnota, [SIRKA_OKNA - 150, 10])

def zobraz_menu(okno, font_nadpis, font_menu, nejlepsi_skore, jmeno_hrace, high_scores):
    """
    Vykreslovací funkce pro úvodní menu hry s pravidly, interaktivním
    jmenovným polem pro záznam uživatele z klávesnice a top listem.
    """
    okno.fill(MODRA_OBLOHA)
    nadpis = font_nadpis.render("Flappy Pták", True, CERNA)
    nadpis_rect = nadpis.get_rect(center=(SIRKA_OKNA/2, 60))
    okno.blit(nadpis, nadpis_rect)

    # Vykreslení aktuálně tvořeného jména (případně placeholder, když je prázdno)
    text_rekord = font_menu.render(f"Rekord: {nejlepsi_skore}", True, CERNA)
    okno.blit(text_rekord, (SIRKA_OKNA/2 + 50, 120))
    
    zobrazene_jmeno = jmeno_hrace if jmeno_hrace else "(napiš své jméno)"
    text_jmeno = font_menu.render(f"Jméno: {zobrazene_jmeno}", True, CERNA)
    okno.blit(text_jmeno, (SIRKA_OKNA/2 + 50, 150))

    # Definice ovládacích prvků do pole, které je poté dynamicky tištěno řádek po řádku prvek po prvku (D.R.Y. princip)
    instrukce = [
        "Enter = spustit hru",
        "Mez. / Šipka nahoru = skok",
        "Mezerník (ve hře) = pauza",
        "Q = konec hry",
        "R = restart po smrti"
    ]
    for i, text in enumerate(instrukce):
        img = font_menu.render(text, True, CERNA)
        okno.blit(img, (20, 120 + i * 30)) # Zvyšování "Y" offsetu

    # Top list render sekce (pouze pokud existuje nějaký záznam list is not empty)
    if high_scores:
        okno.blit(font_menu.render("Nejlepší hráči:", True, CERNA), (20, 280))
        for idx, (j, s) in enumerate(high_scores):
            img = font_menu.render(f"{idx+1}. {j}: {s}", True, CERNA)
            okno.blit(img, (40, 310 + idx * 25))

    pygame.display.update()

def pauza(okno, font_menu):
    """
    Drobná smyčka fungující jako zarážka (pausa). 
    Zastaví veškerou fyziku a čeká jedině na zmáčknutí mezerníku nebo vynesení výjimky na vypnutí celého okna křížkem.
    """
    v_pauze = True
    while v_pauze:
        zprava = font_menu.render("Pauza - Mezerník pro pokračování", True, CERNA)
        rect = zprava.get_rect(center=(SIRKA_OKNA/2, VYSKA_OKNA/2))
        okno.blit(zprava, rect)
        pygame.display.update()
        
        # Intercept eventů během čekání
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    v_pauze = False # Únik zpět do nadřezené herní smyčky loopu
                if event.key == pygame.K_q:
                    pygame.quit(); exit()

# -------------------------------------------------------------------
# Hlavní herní logika a iniciální procedury
# -------------------------------------------------------------------
pygame.init()
okno = pygame.display.set_mode((SIRKA_OKNA, VYSKA_OKNA))
pygame.display.set_caption('Flappy Pták - Fáze 3: Plná Hra')

hodiny = pygame.time.Clock()
# Definovaní rozlišných velikostí fontu z rodiny Bahnschrift textur pro texty
font_skore = pygame.font.SysFont("bahnschrift", 25)
font_menu = pygame.font.SysFont("bahnschrift", 25)
font_nadpis = pygame.font.SysFont("bahnschrift", 50)

# Globální herní variabily persistující mezi hrami v jedné seanci
jmeno_hrace = ""
high_scores, nejlepsi_skore = nacti_skore(SKORE_SOUBOR)

def herni_smycka():
    """ 
    Masivní zapouzdřená funkce držící životní cyklus samotné hratelné pasáže (jednoho pokusu hráče).
    Po úmrtí se přepne do sekce čekání na restart nebo ukončení, kde už je fyzika pozastavena. 
    Lze ji rekurzivně vyvolat přes 'R' pro novou hru.
    """
    global nejlepsi_skore, high_scores, jmeno_hrace

    # Reset parametrů postavy a trubky pro nově započatou instanci
    ptak_x, ptak_y = 50.0, float(VYSKA_OKNA // 2)
    ptak_velikost = 30
    ptak_y_zmena = 0.0
    gravitace = 0.8
    skok = -10.0

    trubka_sirka = 50
    trubka_mezera = 150
    trubka_x = float(SIRKA_OKNA)
    # První trubka je vygenerována v náhodné výšce ihned za oknem
    trubka_vyska = random.randint(50, VYSKA_OKNA - trubka_mezera - 50)
    rychlost = 5.0

    skore = 0
    hra_konci = False
    hra_zavrena = False   # Indikátor pro "Game over obrazovku" a zastavení fyziky

    while not hra_konci:
        # Sub-smyčka reprezentující stav "mrtev" - čeká na restart (r) a volá funkci zápisu HighScore
        while hra_zavrena:
            okno.fill(MODRA_OBLOHA)
            zprava = font_skore.render("Konec hry! Q-Konec nebo R-Znovu", True, CERVENA)
            rect = zprava.get_rect(center=(SIRKA_OKNA/2, VYSKA_OKNA/2))
            okno.blit(zprava, rect)
            zobraz_skore(okno, font_skore, skore)
            zobraz_nejlepsi_skore(okno, font_skore, nejlepsi_skore)
            pygame.display.update()

            for e in pygame.event.get():
                if e.type == pygame.QUIT: 
                    hra_konci = True; hra_zavrena = False
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_q: 
                        hra_konci = True; hra_zavrena = False
                    if e.key == pygame.K_r: 
                        herni_smycka() # Rekurze spouští od začátku
                        return

        # Hlavní aktivní události, dokud hráč žije 
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT: 
                hra_konci = True
            if ev.type == pygame.KEYDOWN:
                # Modifikace Y vektoru = let vzhůru na vyžádání hráče
                if ev.key == pygame.K_SPACE or ev.key == pygame.K_UP: 
                    ptak_y_zmena = skok
                # Delegace pozastavení na nezávislou pauzovací smyčku
                if ev.key == pygame.K_SPACE: 
                    pauza(okno, font_menu)
                if ev.key == pygame.K_ESCAPE: 
                    pauza(okno, font_menu)

        # Trvalý účinek pádu přičítáním zrychlovací hodnoty gravitace na pozici objektu (Fyzika ptáka)
        ptak_y_zmena += gravitace
        ptak_y += ptak_y_zmena

        # Osekávání souřadnice X znamená postupné přesouvání celistvých bariér zprava->doleva (Pohyb trubky)
        trubka_x -= rychlost
        # Jakmile se trubka schová za levou stranu, respawnuje se čerstvá napravo
        if trubka_x < -trubka_sirka:
            trubka_x = SIRKA_OKNA
            trubka_vyska = random.randint(50, VYSKA_OKNA - trubka_mezera - 50)
            skore += 1 # Bodování za přežití překážky

        # Definice logických obdélníků pro snadné knihovní vyhodnocování průniků bodů (Kolize)
        ptak_rect = pygame.Rect(int(ptak_x), int(ptak_y), ptak_velikost, ptak_velikost)
        trubka_horni = pygame.Rect(int(trubka_x), 0, trubka_sirka, trubka_vyska)
        trubka_dolni = pygame.Rect(int(trubka_x), trubka_vyska + trubka_mezera, trubka_sirka, VYSKA_OKNA)

        # Jestliže proťal texturu překážky, dotknul se nebe, anebo políbil dno... umře.
        if ptak_rect.colliderect(trubka_horni) or ptak_rect.colliderect(trubka_dolni) or ptak_y < 0 or ptak_y + ptak_velikost > VYSKA_OKNA:
            # Zavolání refaktorovaného mechanizmu zápisu skóre při konci seance
            uloz_skore(jmeno_hrace, skore)
            # Uzavření přístupu k fyzice - propadne zpět na začátek kódu k cyklu hra_zavrena
            hra_zavrena = True

        # Rendering (Samotné finální kreslení na obrazovku dle spočtené formy)
        okno.fill(MODRA_OBLOHA)
        pygame.draw.rect(okno, ZELENA_TRUBA, trubka_horni)
        pygame.draw.rect(okno, ZELENA_TRUBA, trubka_dolni)
        pygame.draw.rect(okno, ZALTA_PTAK, ptak_rect)

        zobraz_skore(okno, font_skore, skore)
        zobraz_nejlepsi_skore(okno, font_skore, nejlepsi_skore)
        pygame.display.update()
        hodiny.tick(FPS)

# ===================================================================
# START PROGRAMU - ZACHYTÁVÁNÍ JMÉNA V ÚVODNÍ OBRAZOVCE PŘED HROU
# ===================================================================
cekam = True
while cekam:
    for ev_start in pygame.event.get():
        if ev_start.type == pygame.QUIT: 
            pygame.quit(); exit()
        if ev_start.type == pygame.KEYDOWN:
            if ev_start.key == pygame.K_RETURN: 
                cekam = False # Pád do herni_smycka() níže
            elif ev_start.key == pygame.K_BACKSPACE: 
                jmeno_hrace = jmeno_hrace[:-1] # Zkracování stringu zprava operátorem "slice" (-1)
            else:
                # Rozpozná libovolnou natypovanou alfanumerickou klávesu a transformuje ji na charakter UPPERCASE textu
                znak = pygame.key.name(ev_start.key)
                if len(znak) == 1 and len(jmeno_hrace) < 10: 
                    jmeno_hrace += znak.upper()

    # Cyklické tvoření grafiky podkladu nabídky na FPS bází uvnitř prázdného menu
    zobraz_menu(okno, font_nadpis, font_menu, nejlepsi_skore, jmeno_hrace, high_scores)
    hodiny.tick(FPS)

# Otevření vstupní herní sekvence po odklepnutí jména z menu
herni_smycka()

# Celoaplikové odpojení knihovny pygame na konci
pygame.quit()
