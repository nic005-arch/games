import os
import requests


def download_immage(url, filepath):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filepath, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded {filepath}")
    else:
        print(f"Failed to download {url}")

def get_cards(path):
    base_url = "https://deckofcardsapi.com/static/img/"

    # Seme e valori delle carte
    suits = ['C', 'D', 'H', 'S']
    values = ['2', '3', '4', '5', '6', '7', '8', '9', '0', 'J', 'Q', 'K', 'A']

    # Creare la cartella se non esiste
    if not os.path.exists(path):
        os.makedirs('cards')


    for suit in suits:
        for value in values:
            card_code = value + suit
            url = base_url + card_code + ".png"
            filepath = os.path.join('cards', card_code + ".png")
            download_immage(url, filepath)

    download_immage("https://deckofcardsapi.com/static/img/back.png", filepath=os.path.join('cards', "back" + ".png"))
