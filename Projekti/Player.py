import random


class Player():
    def __init__(self, id, name):
        self.id = id
        self.name = name
    def get_id(self):
        return self.id
    def get_nimi(self):
        return self.name


class test():
    def create_player():
        id = random.randint(1,4)
        nimi = input("Nimi: ")
        player = Player(id, nimi)
        return player

    x=create_player()
    print(x.get_id())
    print(x.get_nimi())





