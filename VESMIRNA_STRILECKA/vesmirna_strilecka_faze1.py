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
hrac_rychlost = 6

# hlavní herní smyčka
hra_bezi = True

while hra_bezi:
    for událost in pygame.event.get():
        if událost.type == pygame.QUIT:
            hra_bezi = False

# vykreslení grafiky
okno.fill((0, 0, 0))

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

