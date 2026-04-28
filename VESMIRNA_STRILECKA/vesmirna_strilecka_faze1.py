import pygame
import random

pygame.init( )

sirka = 800
vyska = 800
okno = pygame.display.set_mode((sirka, vyska))
pygame.display.set_caption("Vesmírná střílečka")

# nové vlastnosti hřáče
hrac_x = 375
hrac_y = 700
hrac_sirka = 50
hrac_vyska = 50
hrac_barva = (255, 0, 0)
hrac_rychlost = 4
strely = []


nepratele = []

hvezdy = []

strely_ufonu = []

for i in range(50):
    hvezdy.append([random.randint(0, sirka), random.randint(0, vyska)])

for i in range(5):
    nepratele.append([i * 100 + 50, 50])

# tady létají ufoni
    for ufon in nepratele:
        pygame.draw.rect(okno, (0, 255, 0), (ufon[0], ufon[1], 40, 40))

# hlavní herní smyčka
hra_bezi = True

hodiny = pygame.time.Clock()

skore = 0

zdravi = 123
# font písma aby to bylo pěkné
font = pygame.font.SysFont("cloud bold", 60)

# HLAVNÍ SMYČKA
while hra_bezi:
    hodiny.tick(80) # nastaví rychlos na 80 snímků za sekundu
    if zdravi < 167:
        zdravi += 0.1
    for událost in pygame.event.get():
        if událost.type == pygame.QUIT:
            hra_bezi = False

        # tady děláme to, že když zmáčkneme mezerník, tak se vystřelí
        if událost.type == pygame.KEYDOWN:
            if událost.key == pygame.K_SPACE:
                strely.append([hrac_x, hrac_y])

    # tady se pohybují střely
    for strela in strely:
        strela[1] -= 10 # číslo 10 je rychlost střely a 

    # 1. Sestřelování ufonů (řeší jen střely a ufony)
    for strela in strely[:]:
        strela_rect = pygame.Rect(strela[0] + 20, strela[1], 5, 10)
        
        for ufon in nepratele[:]:
            ufon_rect = pygame.Rect(ufon[0], ufon[1], 40, 40)
            
            # pokud se střely překrývají srazí se 
            if strela_rect.colliderect(ufon_rect):
                if strela in strely:
                    strely.remove(strela)
                if ufon in nepratele:    
                    nepratele.remove(ufon)
                    skore += 1 # přičteme bod za zásah ufona
                break

    # 2. Game over (řeší jen loď hráče a ufony, ODDĚLENO ZLEVA!)
    hrac_rect = pygame.Rect(hrac_x, hrac_y, hrac_sirka, hrac_vyska)
    for strela_u in strely_ufonu[:]:
        strela_u[1] += 7 # rychlost padající ufony půazmy

        # detekujeme jestli žlutý obdelníček mimozemské střely neplácnul o tvou červenou lod
        strela_u_rect = pygame.Rect(strela_u[0] + 17, strela_u[1], 6, 15)
        if hrac_rect.colliderect(strela_u_rect):
            zdravi -= 20 # zasáhli tě odečítáme malý život me 
            strely_ufonu.remove(strela_u) # žlutá plazma se vsákne do tvojí lodi a zmizí
            # kontrola konce hry ůplně stejně, jako to máš u osobních smrtáků nahoře
            if zdravi <= 0:
                napis1 = font.render("GAME OVER", True, (255, 50, 50))
                okno.blit(napis1, (275, 300))
                
                pygame.display.update()

                # můžeme resetovat hru
                napis4 = font.render("HRÁT ZNOVU = Enter", True, (255, 255, 0))
                okno.blit(napis4, (195, 400))

                pygame.display.update()

                cekani = True
                while cekani:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            hra_bezi = False
                            cekani = False
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RETURN: # Pokud zmáčknem R, znova oživneme!
                                zdravi = 167           # Dala sis nový max!
                                skore = 0              # Body naštvaně zase do nuly
                                nepratele = []         # Smažeme všechny fujtajblový Ufony na mapě 
                                strely = []          
                                strely_ufonu = []
                                hrac_x = 375           # Osobní teleport lodě zpět domů
                                hrac_y = 700
                                cekani = False         # Ukončíme pasivní čekání a jedem rubat dál!
                            
                           
               
    
        
       
    for ufon in nepratele[:]:
        ufon_rect = pygame.Rect(ufon[0], ufon[1], 40, 40)
        # narazili jsme do sebe
        if hrac_rect.colliderect(ufon_rect):
            zdravi -= 15 # ufon ti ulomil křídlo (dáme 15 damage)
            nepratele.remove(ufon) # ufon zmizel

            if zdravi <= 0: # když dojdou životy tak konec hry

                # tady se 
               
                napis1 = font.render("GAME OVER", True, (255, 50, 50))
                okno.blit(napis1, (275, 300))
            

                # tady díky toho si můžeme vybrat jestli chceme resetovat hru nebo ukončit
                napis4 = font.render("HRÁT ZNOVU = Enter", True, (255, 255, 0))
                okno.blit(napis4, (195, 400))
                pygame.display.update()

                cekani = True
                while cekani:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            hra_bezi = False
                            cekani = False
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_r: # Pokud zmáčknem R, znova oživneme!
                                zdravi = 167           # Dala sis nový max!
                                skore = 0              # Body naštvaně zase do nuly
                                nepratele = []         # Smažeme všechny fujtajblový Ufony na mapě 
                                strely = []          
                                strely_ufonu = []
                                hrac_x = 375           # Osobní teleport lodě zpět domů
                                hrac_y = 700
                                cekani = False         # Ukončíme pasivní čekání a jedem rubat dál!
                            
                            elif event.key == pygame.K_q: # Pokud zmáčknem flegmanticky Q, jdeme domů...
                                hra_bezi = False
                                cekani = False


    # 3. Nekoneční ufoni (řeší mizení a rození ufonů, ODDĚLENO ZLEVA!)
    for ufon in nepratele[:]:
        if ufon[1] > vyska:
            nepratele.remove(ufon)
            
    if len(nepratele) < 6:
        nove_x = random.randint(0, sirka - 40)
        nepratele.append([nove_x, -40]) # přidání nového ufona

# vykreslení grafiky
    okno.fill((0, 0, 0))

    # kreslení hvězd
    for hvezda in hvezdy:
        hvezda[1] += 1 # hvezda padá pomaličku dolů
        # když doletí dolů, tak se objeví zase nahoře hvězda
        if hvezda[1] > vyska:
            hvezda[1] = 0
            hvezda[0] = random.randint(0, sirka) # náhodné místo kde se objeví hvězda
        # vykreslení samotné hvězdíčky (malimly bílá čtveřeček )
        pygame.draw.circle(okno, (255, 255, 255), (hvezda[0], hvezda[1]), 2)
        

    #kreslení střel
    for strela in strely:
        pygame.draw.rect(okno, (255, 255, 255), (strela[0] + 20, strela[1], 5, 10))

    # TADY vyteklá plazma: Vytiskneme ufoní lasery až pod okno.fill()!! 
    for strela_u in strely_ufonu:
        pygame.draw.rect(okno, (255, 165, 0), (strela_u[0] + 17, strela_u[1], 5, 10))

    # další vrstva barev
    for ufon in nepratele:
        rychlost_ufonu = 2 + (skore / 10)
        ufon[1] += rychlost_ufonu
        pygame.draw.rect(okno, (0, 255, 0), (ufon[0], ufon[1], 40, 40))

        # každý ufon má šanci 1% v každém snímku hry zmáčknou spoušť
        if random.randint(0, 100) == 1:
            # vystřelí to z jeho pomyslného břích směrwm dolů ke mně
            strely_ufonu.append([ufon[0], ufon[1]])

    # nakreslíme hráče
    pygame.draw.rect(okno, hrac_barva, (hrac_x, hrac_y, hrac_sirka, hrac_vyska))

    # text se skóre
    text = font.render("Skóre: " + str(skore), True, (255, 255, 255))
    okno.blit(text, (10, 10))
    
    # nakreslíme to tvrdé červené pozadí délky 246 
    pygame.draw.rect(okno, (255, 0, 0), (0, 750, 246, 50))

    # nakreslíme to tvrdé zelené pozadí které se healuuje a ubývá přesně podle síly tvého zdraví
    if zdravi > 0:
        pygame.draw.rect(okno, (0, 255, 0), (0, 750, zdravi, 50))

    # promítne to na monitor
    pygame.display.update()



    # pohyb hrače a všeho asi idk

    klavesy = pygame.key.get_pressed()

    # menění souřadnic podle toho kam chceme letět
    if klavesy[pygame.K_LEFT]:
        hrac_x -= hrac_rychlost
    if klavesy[pygame.K_RIGHT]:
        hrac_x += hrac_rychlost


    # ošetření okrajů
    if hrac_x < 0:
        hrac_x = 0 # narazí na levý okraj
    if hrac_x > sirka - hrac_sirka:
        hrac_x = sirka - hrac_sirka  # narazi na pravý okraj    

    # to samé pro y
    if klavesy[pygame.K_UP]:
        hrac_y -= hrac_rychlost
    if klavesy[pygame.K_DOWN]:
        hrac_y += hrac_rychlost
    
# vypnutí 
pygame.quit()

