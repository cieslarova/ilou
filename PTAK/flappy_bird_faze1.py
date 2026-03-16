import pygame

# Inicializace knihovny Pygame, což je nezbytné před použitím jejích modulů
pygame.init()

# Definice základních barev pomocí RGB (Red, Green, Blue) hodnot
BILA = (255, 255, 255)
MODRA_OBLOHA = (135, 206, 235)  # Barva pozadí simulující nebe
ZALTA_PTAK = (255, 255, 0)      # Barva hráče

# Nastavení parametrů herního okna
sirka_okna = 600
vyska_okna = 400
# Vytvoření samotného okna a nastavení jeho titulku
okno = pygame.display.set_mode((sirka_okna, vyska_okna))
pygame.display.set_caption('Flappy Pták - Fáze 1: Pohyb')

# Počáteční nastavení vlastností postavy (ptáka)
ptak_x = 50.0                           # Pozice X se v této fázi nemění, pták je fixován vlevo
ptak_y = float(vyska_okna // 2)         # Pozice Y začíná přesně v polovině okna
ptak_velikost = 30                      # Rozměr vykreslovaného čtverce pro ptáka
ptak_y_zmena = 0.0                      # Rychlost pohybu v ose Y (kladná = dolů, záporná = nahoru)

# Fyzikální konstanty ovlivňující pohyb hráče
gravitace = 0.8                         # Síla zrychlení, která ptáka neustále táhne dolů
skok = -10.0                            # Síla skoku (směřuje nahoru, proto je hodnota záporná)

# Objekt pro správu času a FPS
hodiny = pygame.time.Clock()
fps = 30                                # Cílový počet snímků za sekundu, udržuje stejnou rychlost hry

# Hlavní herní smyčka
# Cyklus běží neustále, dokud se nezmění proměnná bezi na False
bezi = True
while bezi:
    # 1. Zpracování uživatelských událostí (klávesnice, okno)
    for event in pygame.event.get():
        # Kontrola, zda uživatel neklikl na křížek pro zavření okna
        if event.type == pygame.QUIT:
            bezi = False
        
        # Zjišťujeme, jestli nebyla stisknuta klávesa
        if event.type == pygame.KEYDOWN:
            # Reakce na stisknutí klávesy Space (mezerník) nebo šipky nahoru (UP)
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                # Při skoku zrušíme aktuální pád a nastavíme rychlost směrem vzhůru
                ptak_y_zmena = float(skok)

    # 2. Fyzika a výpočet nové pozice
    ptak_y_zmena += gravitace           # Aplikace zrychlení (gravitace) na vertikální rychlost
    ptak_y += ptak_y_zmena              # Posun pozice ptáka o vypočtenou rychlost

    # 3. Dodatečné ošetření hranic obrazovky (kolize se stěnami)
    if ptak_y < 0: 
        # Zabránění vyletění nad horní okraj obrazovky
        ptak_y = 0.0
        ptak_y_zmena = 0.0
    if ptak_y + ptak_velikost > vyska_okna: 
        # Zastavení pádu u spodního okraje obrazovky
        ptak_y = float(vyska_okna - ptak_velikost)
        ptak_y_zmena = 0.0

    # 4. Vykreslování (Renderování) aktuálního stavu hry
    # Nejprve vždy překreslíme celou obrazovku barvou oblohy, čímž vymažeme předchozí snímek
    okno.fill(MODRA_OBLOHA)
    
    # Následně nakreslíme ptáka jako žlutý obdélník na aktuálních souřadnicích
    pygame.draw.rect(okno, ZALTA_PTAK, [int(ptak_x), int(ptak_y), ptak_velikost, ptak_velikost])

    # Tato funkce překlopí (aktualizuje) celou obrazovku, aby se zobrazilo to, co jsme právě nakreslili
    pygame.display.update()
    
    # Omezovač snímkové frekvence zajistí, že cyklus nepojede zbytečně rychle
    hodiny.tick(fps)

# Zcela ukončí modul pygame po opuštění herní smyčky
pygame.quit()
