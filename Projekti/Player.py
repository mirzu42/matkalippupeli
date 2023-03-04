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
#ei muuten mitään hajuu tarviiks tätä ees
class Player():
    def __init__(self, id, name):
        self.id = id
        self.name = name
    def get_id(self):
        return self.id
    def get_nimi(self):
        return self.name

class PelaajanHallinta():
    def create_player(self, nimi): # Lisää yhden pelaajan tietokantaan. Default lokaatio Helsinki-Vantaa
        #also menee paskaks jos koittaa tehä yli 5 käyttäjää jostai syyst idk
        sql = "select id from player;"
        kursori = yhteys.cursor()
        kursori.execute(sql)
        tulos = kursori.fetchall()
        if len(tulos)>0:
            id = tulos[-1][0]+1 #viimeinen id + 1
        else:
            id = 1
        #nimi = input("Nimi: ")
        player = Player(id, nimi)
        sql2 = f"insert into player (id, kokonais_pisteet, bensa, nimi, location) values ({id}, 0, 500, '{nimi}', 'EFHK');"

        kursori.execute(sql2)
        print(f"Tietokantaan lisätty pelaaja: \nID: {id}\nKokonaispisteet: 0\nBensa: 500\nNimi:{nimi}\nLocation: EFHK")
        return player
    def delete_all_players(self):
        sql = "delete from player;"
        kursori = yhteys.cursor()
        kursori.execute(sql)
    def tulosta_pelaajat(self):
        sql = "select nimi from player;"
        k = yhteys.cursor()
        k.execute(sql)
        x = k.fetchall()
        for i in range(len(x)):
            print(x[i][0])
    def paivitaLokaatio(self, icao, p_id):
        sql = f"UPDATE player SET location = '{icao}' WHERE id = '{p_id}'"
        cursor = yhteys.cursor(dictionary=True)  # mitä tää dictionary ees tekee
        cursor.execute(sql)

    def pelaajaAloitus(self):
        sql = "select airport.ident from airport inner join country on airport.iso_country = country.iso_country where country.name = 'Finland' and type != 'closed' and type !='heliport' and type !='small_airport';"
        kursori = yhteys.cursor()
        kursori.execute(sql)
        tulokset = kursori.fetchall()

        if tulokset:
            aloituslokaatio = random.choice(tulokset)[0]
            return aloituslokaatio
        print(tulokset)









