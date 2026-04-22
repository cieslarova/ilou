import pygame

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
hrac_rychlost = 1
strely = []


nepratele = []

for i in range(5):
    nepratele.append([i * 100 + 50, 50])

# tady létají ufoni
    for ufon in nepratele:
        pygame.draw.rect(okno, (0, 255, 0), (ufon[0], ufon[1], 40, 40))

# hlavní herní smyčka
hra_bezi = True

while hra_bezi:
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
    
# vykreslení grafiky
    okno.fill((0, 0, 0))

    #kreslení střel
    for strela in strely:
        pygame.draw.rect(okno, (255, 255, 255), (strela[0] + 20, strela[1], 5, 10))

    # další vrstva barev
    for ufon in nepratele:
        ufon[1] += 2
        pygame.draw.rect(okno, (0, 255, 0), (ufon[0], ufon[1], 40, 40))

    # nakreslíme hráče
    pygame.draw.rect(okno, hrac_barva, (hrac_x, hrac_y, hrac_sirka, hrac_vyska))

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

