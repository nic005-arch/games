import pygame
import sys
import random
import time

# Definire colori
BIANCO = (255, 255, 255)
VERDE = (0, 255, 0)
ROSSO = (255, 0, 0)
NERO = (0, 0, 0)

# Stato iniziale del gioco
stato = ['menu']

# Variabili globali per il saldo e la scommessa
saldo = 1000  # Saldo iniziale
puntata = 0
risultato = ""
global amount
ammount = 100
last_click_time = 0
click_delay = 0.25  # Secondi

pygame.font.init()
font = pygame.font.SysFont('Arial', 35)

# Funzioni di utilità
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def draw_Text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def create_button(text, x, y, width, height, color, hover_color, action, surface):
    global last_click_time
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(surface, hover_color, (x, y, width, height), border_radius=10)
        if click[0] == 1 and time.time() - last_click_time > click_delay:
            last_click_time = time.time()
            action()
    else:
        pygame.draw.rect(surface, color, (x, y, width, height), border_radius=10)
    
    # Disegna il bordo del pulsante
    border_color = (200, 200, 200)  # Colore del bordo
    pygame.draw.rect(surface, border_color, (x, y, width, height), 2, border_radius=10)
    
    # Disegna l'ombra
    shadow_offset = 5
    shadow_color = (50, 50, 50)  # Colore dell'ombra
    pygame.draw.rect(surface, shadow_color, (x + shadow_offset, y + shadow_offset, width, height), border_radius=10)
    
    # Centra il testo nel pulsante
    text_surf = font.render(text, True, BIANCO)
    text_rect = text_surf.get_rect(center=(x + width // 2, y + height // 2))
    surface.blit(text_surf, text_rect)



def quit_game():
    pygame.quit()
    sys.exit()

def start_game(stato):
    stato[0] = 'bet'

def game_menu(win, stato):
    create_button('Start Game', 80, 170, 250, 50, VERDE, ROSSO, lambda: start_game(stato), win)
    create_button('Quit', 80, 270, 250, 50, VERDE, ROSSO, quit_game, win)

def increase_bet():
    global puntata
    if puntata + 100 <= saldo:
        puntata += 100

def decrease_bet():
    global puntata
    if puntata >= 100:
        puntata -= 100

def bet_screen(win):
    draw_Text(f'Saldo corrente: {saldo}', font, BIANCO, win, 150, 15)
    draw_Text(f'Scommessa: {puntata}', font, BIANCO, win, 525, 15)
    create_button('Aumenta', 50, 535, 200, 50, VERDE, ROSSO, increase_bet, win)
    create_button('Diminuisci', 400, 535, 200, 50, VERDE, ROSSO, decrease_bet, win)
    create_button('Conferma', 750, 535, 200, 50, VERDE, ROSSO, lambda: place_bet(puntata , win), win)
    create_button('menu', 860, 10, 100, 50, VERDE, ROSSO, lambda: set_stato('menu'), win)


def set_stato(new_state):
    stato[0] = new_state


def game_screen(win):
    display_game(win)
    create_button('Hit', 600, 525, 150, 50, VERDE, ROSSO, lambda : hit(win), win)
    create_button('Stand', 800, 525, 150, 50, VERDE, ROSSO, lambda: stand(win), win)



# Funzioni del gioco NEROjack
player_hand = []
dealer_hand = []
deck = []

def initialize_deck():
    global deck
    suits = ['H', 'D', 'C', 'S']
    values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    deck = [{'suit': suit, 'value': value} for suit in suits for value in values]
    random.shuffle(deck)

def draw_card(hand):
    global deck
    card = deck.pop()
    hand.append(card)

def calculate_hand_value(hand):
    value = 0
    num_aces = 0
    value_map = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}
    for card in hand:
        value += value_map[card['value']]
        if card['value'] == 'A':
            num_aces += 1
    while value > 21 and num_aces:
        value -= 10
        num_aces -= 1
    return value

def initialize_game(win):
    global player_hand, dealer_hand
    player_hand = []
    dealer_hand = []
    initialize_deck()
    draw_card(player_hand)
    draw_card(player_hand)
    draw_card(dealer_hand)
    draw_card(dealer_hand)
    check_for_bust(win)
    check_for_NEROjack(win)

def place_bet( amount , win):
    global saldo, puntata, stato
    if amount <= saldo and amount > 0:
        saldo -= amount
        stato[0] = 'game'
        initialize_game(win)
    else:
        print("Non hai abbastanza chips per questa scommessa.")

def hit(win):
    draw_card(player_hand)
    check_for_bust(win)

def stand(win):
    global stato
    # Scopri la prima carta del dealer
    card_image_path = f"assets/cards/{dealer_hand[0]['value']}{dealer_hand[0]['suit']}.png"
    dealer_hand[0]['image'] = pygame.image.load(card_image_path)
    
    # Mostra la carta scoperta
    stato[0] = 'reveal_dealer_card'
    display_game(win)
    pygame.display.update()
    time.sleep(3)

    # Continua con il gioco dopo aver mostrato la carta
    while calculate_hand_value(dealer_hand) < 17:
        draw_card(dealer_hand)
        display_game(win)
        pygame.display.update()
        time.sleep(1)  # Pausa per vedere il dealer che pesca una carta

    determine_winner(win)


def check_for_bust(win):
    if calculate_hand_value(player_hand) > 21:
        print("Il giocatore ha sballato! Il tavolo vince!")
        stato[0] = 'show_result'
        show_result("Il tavolo vince ", win)

def check_for_NEROjack(win):
    global stato, saldo, puntata, risultato
    player_value = calculate_hand_value(player_hand)
    dealer_value = calculate_hand_value(dealer_hand)

    if player_value == 21:
        if dealer_value == 21:
            risultato = "Sia il tavolo che il giocatore hanno Blackjack! Pareggio."
            saldo += puntata  # Restituisce la scommessa in caso di pareggio
        else:
            risultato = "Il giocatore ha Blackjack! Il giocatore vince!"
            saldo += puntata * 2.5  # Pagamento 3:2 per il NEROjack
    elif dealer_value == 21:
        risultato = "il tavolo ha Blackjack! Il tavolo vince!"
    else:
        return  # Se nessuno ha NEROjack, non fare nulla

    puntata = 0
    stato[0] = 'show_result'
    show_result(risultato, win)



def determine_winner(win):
    global saldo, puntata, risultato
    player_value = calculate_hand_value(player_hand)
    dealer_value = calculate_hand_value(dealer_hand)

    if dealer_value > 21 or player_value > dealer_value:
        risultato = "Player wins!"
        saldo += puntata * 2  # Il giocatore vince il doppio della scommessa
    elif player_value < dealer_value:
        risultato = "Dealer wins!"
    else:
        risultato = "It's a tie!"
        saldo += puntata  # Restituisce la scommessa in caso di pareggio

    puntata = 0

    # Mostra il risultato dopo 3 secondi
    show_result(risultato, win)


def show_result(message, win):
    global stato
    start_time = time.time()
    while time.time() - start_time < 3:
        win.fill(NERO)
        draw_text(message, font, BIANCO, win, 500, 300)
        pygame.display.update()
    stato[0] = 'bet'



def display_game(win):
    font = pygame.font.SysFont('Arial', 30)

    # Mostrare il saldo del giocatore
    draw_Text(f'Saldo: {saldo}', font, BIANCO, win, 20, 5)
    draw_Text(f'Scommessa: {puntata}', font, BIANCO, win, 20, 35)
    draw_Text(f'Punteggio mano giocatore: {calculate_hand_value(player_hand)}', font, BIANCO, win, 20, 550)


    # Posizionare le carte del giocatore
    x_offset = 430
    y_offset = 285
    for card in player_hand:
        card_image_path = f"assets/cards/{card['value']}{card['suit']}.png"
        try:
            card_image = pygame.image.load(card_image_path)
            card_image = pygame.transform.scale(card_image, (80, 100))  # Ridimensiona la carta
            win.blit(card_image, (x_offset, y_offset))
        except pygame.error:
            print(f"Errore nel caricamento dell'immagine: {card_image_path}")
        x_offset += 60

    # Posizionare le carte del dealer
    x_offset = 430
    y_offset = 150
    for i, card in enumerate(dealer_hand):
        if i == 0 and stato[0] != 'reveal_dealer_card':
            card_image_path = "assets/cards/back.png"  # Carta coperta
        else:
            card_image_path = f"assets/cards/{card['value']}{card['suit']}.png"
        try:
            card_image = pygame.image.load(card_image_path)
            card_image = pygame.transform.scale(card_image, (80, 100))  # Ridimensiona la carta
            win.blit(card_image, (x_offset, y_offset))
        except pygame.error:
            print(f"Errore nel caricamento dell'immagine: {card_image_path}")
        x_offset += 60
