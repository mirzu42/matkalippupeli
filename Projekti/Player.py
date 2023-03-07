import random
import mysql.connector
from Kortit import *
from Lentokenttienhaku import *
from Lippu import *
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

kh =KortinHallinta()

yhteys = mysql.connector.connect(
         host="127.0.0.1",
         port= 3306,
         database="matkalippupeli",
         user="root",
         password="1234",
         autocommit=True
         )

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
        kh.createMultipleKortti(3, id)
       # print(f"Tietokantaan lisätty pelaaja: \nID: {id}\nKokonaispisteet: 0\nBensa: 500\nNimi:{nimi}\nLocation: EFHK")
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
    def getNimi(self, p_id):
        sql = f"select nimi from player where id = {p_id};"
        cursor = yhteys.cursor()
        cursor.execute(sql)
        x = cursor.fetchone()
        return x[0]


    def paivitaLokaatio(self, icao, pelaaja_id):
        sql = f"UPDATE player SET location = '{icao}' WHERE id = '{pelaaja_id}'"
        cursor = yhteys.cursor(dictionary=True)  # mitä tää dictionary ees tekee
        cursor.execute(sql)

    def getPelaajanLokaatio(self, p_id):
        sql = f"Select location from player where id = '{p_id}'"
        cursor = yhteys.cursor()
        cursor.execute(sql)
        tulos = cursor.fetchone()
        return tulos[0]

    '''def pelaajaAloitus(self): #ei salee tarvita tätä? lippu() tekee jo muutenki randomil ton
        sql = "select airport.ident from airport inner join country on airport.iso_country = country.iso_country where country.name = 'Finland' and type != 'closed' and type !='heliport' and type !='small_airport';"
        kursori = yhteys.cursor()
        kursori.execute(sql)
        tulokset = kursori.fetchall()

        if tulokset:
            aloituslokaatio = random.choice(tulokset)[0]
            return aloituslokaatio
        print(tulokset)
    def uusiPelaajanLippu(self, pelaaja_id, lippu_id):
        sql = f"insert into pelaajan_liput (player_id, liput_id) values ({pelaaja_id}, {lippu_id})"
        cursor = yhteys.cursor()
        cursor.execute(sql)
        print(f"Tietokantaan lisätty pelaajan lippu: \nlippuID: {lippu_id}\nPelaajaID: {pelaaja_id}")'''

    def delete_all_pelaajanLiput(self):
        sql = "delete from pelaajan_liput;"
        kursori = yhteys.cursor()
        kursori.execute(sql)
    def kaytaPelaajanKortti(self, kortti_tyyppi, pelaaja_id):
        sql1 = f" select kortit.id from kortit inner join pelaajan_kortit on pelaajan_kortit.kortti_id = kortit.id where player_id = {pelaaja_id} and kortit.tyyppi = '{kortti_tyyppi}' order by kortit.id desc limit 1;"
        cursor = yhteys.cursor()
        cursor.execute(sql1)
        muuttuja = cursor.fetchone()

        sql2 = f"select kortit.id from kortit inner join pelaajan_kortit on pelaajan_kortit.kortti_id = kortit.id where player_id = {pelaaja_id} and kortit.tyyppi = 'jokeri';"
        cursor.execute(sql2)

        ookkoNääPorvari = self.onkoPelaajaPaVaiPorvari(pelaaja_id, kortti_tyyppi, 1)
        if ookkoNääPorvari == True :
            sql3 = f"delete from pelaajan_kortit where kortti_id = '{muuttuja[0]}';"
            cursor.execute(sql3)
            sql4 = f"delete from kortit where id = '{muuttuja[0]}';"
            cursor.execute(sql4)
            self.bensaKulutus(pelaaja_id, 1)
        else:
            print("Vittu sää oot köyhä")

    def onkoPelaajaPaVaiPorvari(self, pelaaja_id, kortinVari, tarvittavaLkm):
        sql = f"select count(*) as pelaajan_korttien_lkm from pelaajan_kortit inner join kortit on id = kortti_id where tyyppi = '{kortinVari}' and player_id = '{pelaaja_id}';"
        cursor = yhteys.cursor()
        cursor.execute(sql)
        tulos = cursor.fetchone()
        if tulos[0] >= tarvittavaLkm:
            return True
            #Pelaaja on porvari
        else:
            return False
            #Pelaaja on persaukinen :)

    def kaytaMontaKorttia(self, lkm,  kortti_tyyppi, pelaaja_id):
        ookkoNääPorvari = self.onkoPelaajaPaVaiPorvari(pelaaja_id, kortti_tyyppi, lkm)
        if ookkoNääPorvari == True :
            for i in range(lkm):
                self.kaytaPelaajanKortti(kortti_tyyppi, pelaaja_id)
        else:
            print("Vitun köyhä :-D")

    def bensaKulutus(self, player_id, korttiLkm):
        sql1 = f"update player set bensa = bensa - 8 * '{korttiLkm}' where id = '{player_id}';"
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

    def getPelaajanKortit(self, p_id):
        sql =f"select player_id, tyyppi, count(tyyppi) from pelaajan_kortit, kortit where id= kortti_id and player_id = {p_id} group by tyyppi;"
        cursor =yhteys.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()

        print(bcolors.WARNING+f"Pelaajalla {self.getNimi(p_id)} on: ")
        for i in result:
            print (bcolors.OKBLUE,+i[2],"x", i[1])

    def getPelaajanLiput(self, pelaaja_id):
        sql = f"select lähtö, kohde from liput inner join pelaajan_liput on id=liput_id where player_id = '{pelaaja_id}';"
        cursor = yhteys.cursor()
        cursor.execute(sql)
        tulokset = cursor.fetchall()

        tmp = self.getNimi(pelaaja_id)
        #print(f'Pelaajan {tmp} liput:')

        for tulos in tulokset:
            sql2 = f"select name from airport where ident = '{tulos[0]}'"
            cursor.execute(sql2)
            lahtoICAO = cursor.fetchone()
            sql3 = f"select name from airport where ident = '{tulos[1]}'"
            cursor.execute(sql3)
            kohdeICAO = cursor.fetchone()

            print(bcolors.WARNING + f'Pelaajan {tmp} lippu:''\n''\tLähtö:', lahtoICAO[0], '\n''\tKohde:', kohdeICAO[0])
            #print('\tLähtö:', lahtoICAO[0], '\n\tKohde:', kohdeICAO[0])
            print()
       # tmp = self.getNimi(pelaaja_id)


    # Alemmat funktiot vaativat lisätietoa. PelaajanAloitus tarvitsee jostain lipusta vaihtoehdot
        # Liike tarvitsee jostain parametrit saavutettaviin lentokenttiin


    def PelaajaAloitusPaikkaValinta(self, pelaaja_id):

        lipun_hallinta = LipunHallinta()
        lippu1 = lipun_hallinta.createLippu(pelaaja_id)
        lippu2 = lipun_hallinta.createLippu(pelaaja_id)

        print(f"Valitse lippu:")
        print(f"1. {lippu1}")
        print(f"2. {lippu2}")
        try:
            while True:
                syote = int(input())
                if (syote == 1):
                    valinta = lippu1
                    break
                elif (syote==2):
                    valinta = lippu2
                    break
                else:
                    print("Virheellinen syöte!")

        except:
            print("Virheellinen syöte!")

        #päivitetään pelaajan sijainti
        sql = f"select ident from airport where name = '{valinta[0]}';"
        cursor = yhteys.cursor()
        cursor.execute(sql)
        tulos = cursor.fetchone()
        self.paivitaLokaatio(tulos[0], pelaaja_id)
        #return tulos[0]


    def Liike(self, p_id):
        while True:
            icao = self.getPelaajanLokaatio(p_id)
            korttien_lkm = kh.getLentokenttaKorttien_lkm(icao)
            self.bensaKulutus(p_id, korttien_lkm)
            print("Voit liikkua seuraaville lentokentille:")
            lentokentät = saavutettavatLentokentat(icao)
            valinta = 0
            while valinta < 1 or valinta > 5:
                try:
                    valinta = int(input("Valitse lentokenttä (1-5): "))
                except ValueError:
                    print("Syötä numero")
            if valinta:
                icao = lentokentät[valinta - 1]['ident']
                self.paivitaLokaatio(icao, p_id)
                print("Siirrytty kentälle: ", lentokentät[valinta - 1]['name'])
                matka = lentokentät['distance']
                korttien_lkm += (matka // 62) * 6
                KortinHallinta.VähennäPelaajanKortteja(p_id, korttien_lkm)

        return lentokentät[valinta - 1]['ident']


