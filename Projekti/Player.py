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
'''class Player():
    def __init__(self, id, name):
        self.id = id
        self.name = name
    def get_id(self):
        return self.id
    def get_nimi(self):
        return self.name'''

class PelaajanHallinta():
    def create_player(self, nimi): # Lisää yhden pelaajan tietokantaan. Default lokaatio Helsinki-Vantaa

        sql = "select id from player;"
        kursori = yhteys.cursor()
        kursori.execute(sql)
        tulos = kursori.fetchall()
        if len(tulos)>0:
            id = tulos[-1][0]+1 #viimeinen id + 1
        else:
            id = 1
        #nimi = input("Nimi: ")
        #player = Player(id, nimi)
        sql2 = f"insert into player (id, kokonais_pisteet, bensa, nimi, location) values ({id}, 0, 500, '{nimi}', 'EFHK');"

        kursori.execute(sql2)
        print(f"Tietokantaan lisätty pelaaja: \nID: {id}\nKokonaispisteet: 0\nBensa: 500\nNimi:{nimi}\nLocation: EFHK")
        #return player


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

    def pelaajaAloitus(self): #ei salee tarvita tätä? lippu() tekee jo muutenki randomil ton
        sql = "select airport.ident from airport inner join country on airport.iso_country = country.iso_country where country.name = 'Finland' and type != 'closed' and type !='heliport' and type !='small_airport';"
        kursori = yhteys.cursor()
        kursori.execute(sql)
        tulokset = kursori.fetchall()

        if tulokset:
            aloituslokaatio = random.choice(tulokset)[0]
            return aloituslokaatio
        print(tulokset)

    '''def uusiPelaajanKortti(self, pelaaja_id, kortti_id):
        sql = f"insert into pelaajan_kortit (kortti_id, player_id) values ({pelaaja_id}, {kortti_id});"
        cursor = yhteys.cursor()
        cursor.execute(sql)
        print (f"Tietokantaan lisätty pelaajan kortti: \nKortti_id: {kortti_id}\npelaaja_id: {pelaaja_id}")'''
    def delete_all_pelaajankortit(self):
        sql = "delete from pelaajan_kortit;"
        kursori = yhteys.cursor()
        kursori.execute(sql)
    def uusiPelaajanLippu(self, pelaaja_id, lippu_id):
        sql = f"insert into pelaajan_liput (player_id, liput_id) values ({pelaaja_id}, {lippu_id})"
        cursor = yhteys.cursor()
        cursor.execute(sql)
        print(f"Tietokantaan lisätty pelaajan lippu: \nlippuID: {lippu_id}\nPelaajaID: {pelaaja_id}")

    def delete_all_pelaajanLiput(self):
        sql = "delete from pelaajan_liput;"
        kursori = yhteys.cursor()
        kursori.execute(sql)
    def kaytaPelaajanKortti(self, kortti_tyyppi, pelaaja_id):
        sql = f"delete t1 from pelaajan_kortit AS t1 INNER JOIN kortit AS t2 ON t1.kortti_id = t2.id where t2.tyyppi = '{kortti_tyyppi}' and t1.player_id = {pelaaja_id};"
        cursor = yhteys.cursor()
        cursor.execute(sql)
        #pitää viel käytää bensaa
    def bensakulutus(self, player_id, lkm):
        sql1 = f"update player set bensa = bensa - 8 * '{lkm}' where id = '{player_id}';"
        sql2 = f"select bensa from player where id = '{player_id}';"
        kursori = yhteys.cursor()
        kursori.execute(sql1)
        kursori.execute(sql2)
        result = kursori.fetchone()
        bensa = result[0]
        return bensa
    def getId(self, nimi):
        getid = f"select id from player where nimi = '{nimi}';"
        cursor = yhteys.cursor()
        cursor.execute(getid)
        x = cursor.fetchone()


        return x[0]


