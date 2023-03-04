import random
import mysql.connector
yhteys = mysql.connector.connect(
         host="127.0.0.1",
         port= 3306,
         database="matkalippupeli",
         user="root",
         password="1234",
         autocommit=True
         )
class Player():
    def __init__(self, id, name):
        self.id = id
        self.name = name
    def get_id(self):
        return self.id
    def get_nimi(self):
        return self.name


def create_player(): # Lisää yhden pelaajan tietokantaan. Default lokaatio Helsinki-Vantaa

    sql = "select id from player;"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchall()
    if len(tulos)>0:
        id = tulos[-1][0]+1 #viimeinen id + 1
    else:
        id = 1
    nimi = input("Nimi: ")
    player = Player(id, nimi)
    sql2 = f"insert into player (id, kokonais_pisteet, bensa, nimi, location) values ({id}, 0, 500, '{nimi}', 'EFHK');"

    kursori.execute(sql2)
    return player
def delete_all_players():
    sql = "delete from player;"
    kursori = yhteys.cursor()
    kursori.execute(sql)


create_player()



