from Player import Player
import random


def create_player():
    id = random.randint(1, 4)
    nimi = input("Nimi: ")
    player = Player(id, nimi)
    return player
x = create_player()
print(x.get_id())
print(x.get_nimi())