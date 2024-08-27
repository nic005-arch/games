global stato
global ammount
from time import sleep
import pygame
import sys
from libs.start import *
from assets import c 

if not os.path.exists("./assets/cards"):
    print("Carte non trovate, estraggo le carte")
    c.get_cards("./assets/cards")


pygame.init()
pygame.font.init()

# Caricare immagine di sfondo per il menu iniziale
start = pygame.image.load('./assets/inizio.jpeg')
start = pygame.transform.scale(start, (1000, 600))

# Caricare immagine di sfondo per il gioco
background = pygame.image.load('./assets/tavolo.jpeg')
background = pygame.transform.scale(background, (1000, 600))

# Impostare dimensioni finestra
win = pygame.display.set_mode((background.get_width(), background.get_height()))
pygame.display.set_caption("Blacljack")

# Ciclo principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                increase_bet()
            elif event.key == pygame.K_DOWN:
                decrease_bet()
            elif event.key == pygame.K_RETURN:
                place_bet(puntata , win)

    # Disegnare sfondo
    if stato[0] == 'menu':
        win.blit(start, (0, 0))
        game_menu(win, stato)
    elif stato[0] == 'bet':
        win.blit(background, (0, 0))
        bet_screen(win)
    elif stato[0] == 'game':
        win.blit(background, (0, 0))
        game_screen(win)
    elif stato[0] == 'online_game':
        pass
    elif stato[0] == 'reveal_dealer_card':
            display_game(win) 

    pygame.display.update()

pygame.quit()
