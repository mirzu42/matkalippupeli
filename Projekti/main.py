from Player import Player
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

def create_player(): # Lisää yhden pelaajan tietokantaan. Default lokaatio Helsinki-Vantaa

    sql = "select id from player;"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchall()

    id = tulos[-1][0]+1 #viimeinen id + 1
    nimi = input("Nimi: ")
    player = Player(id, nimi)
    sql2 = f"insert into player (id, kokonais_pisteet, bensa, nimi, location) values ({id}, 0, 500, '{nimi}', 'EFHK');"

    kursori.execute(sql2)
    return player
x = create_player()
print(x.get_id())
print(x.get_nimi())

