
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
lh = LipunHallinta()
BENSA = 500

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

        sql2 = f"insert into player (id, kokonais_pisteet, bensa, nimi) values ({id}, 0, '{BENSA}', '{nimi}');"

        kursori.execute(sql2)
        self.pelaajanAloituksenLippujenValinta(id)

    def getAllPelaajat(self):
        sql = "select nimi from player;"
        cursor = yhteys.cursor()
        cursor.execute(sql)
        tulos = cursor.fetchall()
        return tulos


    def delete_all_players(self):  #poistaa kaikki pelaajat
        sql = "delete from player;"
        kursori = yhteys.cursor()
        kursori.execute(sql)


    def tulosta_pelaajat(self):  #tulostaa pelaajat
        sql = "select nimi from player;"
        cursor = yhteys.cursor()
        cursor.execute(sql)
        tulos = cursor.fetchall()
        for i in range(len(tulos)):
            print(tulos[i][0])


    def getNimi(self, p_id):  #hakee pelaajan nimen tämän pelaaja id:llä
        sql = f"select nimi from player where id = {p_id};"
        cursor = yhteys.cursor()
        cursor.execute(sql)
        tulos = cursor.fetchone()
        return tulos[0]

    def paivitaLokaatio(self, icao, pelaaja_id):  #päivittää pelaajan lokaation parametrissä annetun icao koodin mukaisesti
        sql = f"UPDATE player SET location = '{icao}' WHERE id = '{pelaaja_id}'"
        cursor = yhteys.cursor(dictionary=True)
        cursor.execute(sql)

    def getPelaajanLokaatio(self, p_id):  #hakee pelaajan tämänhetkisen lokaation
        sql = f"Select location from player where id = '{p_id}'"
        cursor = yhteys.cursor()
        cursor.execute(sql)
        tulos = cursor.fetchone()
        return tulos[0]

    def delete_all_Liput(self):  #poistaa kaikki liput ja pelaajan liput
        sql = "delete from pelaajan_liput;"
        kursori = yhteys.cursor()
        kursori.execute(sql)
    def kaytaPelaajanKortti(self, kortti_tyyppi, pelaaja_id):  #käyttää pelaajalta tietyn värisen kortin ja poistaa sen häneltä
        sql1 = f" select kortit.id from kortit inner join pelaajan_kortit on pelaajan_kortit.kortti_id = kortit.id where player_id = {pelaaja_id} and kortit.tyyppi = '{kortti_tyyppi}' order by kortit.id desc limit 1;"
        cursor = yhteys.cursor()
        cursor.execute(sql1)
        muuttuja = cursor.fetchone()

        #jokerikortin käyttämisen toiminnallisuus:
        sql2 = f"select kortit.id from kortit inner join pelaajan_kortit on pelaajan_kortit.kortti_id = kortit.id where player_id = {pelaaja_id} and kortit.tyyppi = 'jokeri';"
        cursor.execute(sql2)

        #tsekkaa onko pelaajalla tarpeeksi tietyn väristä korttia
        onkoVaraa = self.onkoPelaajallaVaraa(pelaaja_id, kortti_tyyppi, 1)
        if onkoVaraa == True :
            sql3 = f"delete from pelaajan_kortit where kortti_id = '{muuttuja[0]}';"
            cursor.execute(sql3)
            sql4 = f"delete from kortit where id = '{muuttuja[0]}';"
            cursor.execute(sql4)
            self.bensaKulutus(pelaaja_id, 1)
        else:
            print("Sinulla ei ole tarpeeksi montaa samanväristä korttia")

    def onkoPelaajallaVaraa(self, pelaaja_id, kortinVari, tarvittavaLkm):  #Tarkistaa onko pelaajalla tarvittava lkm tietynväristä korttia
        sql = f"select count(*) as pelaajan_korttien_lkm from pelaajan_kortit inner join kortit on id = kortti_id where tyyppi = '{kortinVari}' and player_id = '{pelaaja_id}';"
        cursor = yhteys.cursor()
        cursor.execute(sql)
        tulos = cursor.fetchone()
        if tulos[0] >= tarvittavaLkm:
            return True
            #Pelaajalla on tarpeeksi samanvärisiä kortteja/varaa
        else:
            return False
            #Pelaajalla ei ole tarpeeksi samanvärisiä kortteja/varaa

    def kaytaMontaKorttia(self, lkm,  kortti_tyyppi, pelaaja_id):
        onkoVaraa = self.onkoPelaajallaVaraa(pelaaja_id, kortti_tyyppi, lkm)
        if onkoVaraa == True :
            for i in range(lkm):
                self.kaytaPelaajanKortti(kortti_tyyppi, pelaaja_id)
        else:
            print("Sinulla ei ole tarpeeksi montaa samanväristä korttia")

    def bensaKulutus(self, player_id, korttiLkm):  #kuluttaa bensaa käytettyjen korttien lukumäärän mukaan
        sql1 = f"update player set bensa = bensa - 8 * '{korttiLkm}' where id = '{player_id}';"
        sql2 = f"select bensa from player where id = '{player_id}';"
        kursori = yhteys.cursor()
        kursori.execute(sql1)
        kursori.execute(sql2)
        result = kursori.fetchone()
        return result[0]

    def getId(self, nimi):  #palauttaa pelaajan id:n
        getid = f"select id from player where nimi = '{nimi}';"
        cursor = yhteys.cursor()
        cursor.execute(getid)
        result = cursor.fetchone()
        return result[0]

    def getPelaajanKortit(self, p_id):  #tulostaa pelaajan kortit
        sql =f"select player_id, tyyppi, count(tyyppi) from pelaajan_kortit, kortit where id= kortti_id and player_id = {p_id} group by tyyppi;"
        cursor =yhteys.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()

        print(bcolors.OKBLUE+f"Pelaajalla{bcolors.FAIL} {self.getNimi(p_id)}{bcolors.OKBLUE} on: ")
        for i in result:
            if (i[1] == "punainen"):
                print (bcolors.FAIL,+i[2],"x" ,i[1],bcolors.OKBLUE)
            elif(i[1] =="sininen"):
                print(bcolors.OKBLUE, +i[2], "x", i[1])
            elif (i[1] == "keltainen"):
                print(bcolors.WARNING, +i[2], "x", i[1], bcolors.OKBLUE)
            elif (i[1]=="jokeri"):
                print(bcolors.FAIL, +i[2], f"{bcolors.WARNING}x", f"{bcolors.OKBLUE}j{bcolors.WARNING}o{bcolors.FAIL}k{bcolors.OKBLUE}e{bcolors.WARNING}r{bcolors.FAIL}i{bcolors.OKBLUE}")
        print("\n")

    def getPelaajanLiput(self, pelaaja_id):  #tulostaa pelaajalla olevat liput
        sql = f"select lähtö, kohde from liput inner join pelaajan_liput on id=liput_id where player_id = '{pelaaja_id}';"
        cursor = yhteys.cursor()
        cursor.execute(sql)
        tulokset = cursor.fetchall()

        tmp = self.getNimi(pelaaja_id)

        for tulos in tulokset:

            sql2 = f"select name from airport where ident = '{tulos[0]}';"  #hakee lipun lähtöpaikan nimen
            cursor.execute(sql2)
            lahtoICAO = cursor.fetchone()
            sql3 = f"select name from airport where ident = '{tulos[1]}';"  #hakee lipun kohteen nimen
            cursor.execute(sql3)
            kohdeICAO = cursor.fetchone()
            sqlforid = f"select id from liput inner join pelaajan_liput on id = liput_id where lähtö = '{tulos[0]}' and kohde = '{tulos[1]}' and player_id = {pelaaja_id};"
            cursor.execute(sqlforid)
            idlist = cursor.fetchone()
            id = idlist[0]
            sql4 = f"select pisteet from liput inner join pelaajan_liput on id=liput_id where player_id = {pelaaja_id} and liput_id= {id};"
            cursor.execute(sql4)
            pisteet = cursor.fetchall()

            print(bcolors.WARNING + f'Pelaajan {tmp} lippu:''\n''\tLähtö:', lahtoICAO[0], '\n''\tKohde:', kohdeICAO[0],'\n''\tPisteet:', pisteet[0][0])
            print()



    def pelaajanLipunValinta(self, pelaaja_id):  #arvottavien menolippujen valinta

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


    def pelaajanLiike(self, p_id):
        sql = f"select kohde from liput inner join pelaajan_liput on id = liput_id where player_id = {p_id}"
        cursor = yhteys.cursor()
        cursor.execute(sql)
        tulos = cursor.fetchall()
        for i in tulos:
            if i == self.getPelaajanLokaatio(p_id):
                sql2 = f"select pisteet from liput inner join pelaajan_liput on id = liput_id where player_id = {p_id} and kohde ='{i}';"
                cursor.execute(sql2)
                x = cursor.fetchone()
                sql3 = f"update player set kokonais_pisteet = kokonais_pisteet +{x[0]} where id = {p_id};"
                cursor.execute(sql3)
        icao = self.getPelaajanLokaatio(p_id)
        korttien_lkm = kh.getLentokenttaKorttien_lkm(icao)
        #self.kaytaMontaKorttia(korttien_lkm,)
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
            print(lentokentät)
            matka = lentokentät[valinta - 1]['distance_kortit']
            korttien_lkm += (matka // 62) * 6
            kh.vahennaPelaajanKortteja(p_id, korttien_lkm)
        return lentokentät[valinta - 1]['ident']

    def luoAloitusliput(self, pelaaja_id):
        lipun_hallinta = LipunHallinta()
        lippu1 = lipun_hallinta.createLippu(pelaaja_id)
        lippu2 = lipun_hallinta.createLippu(pelaaja_id)
        lippu3 = lipun_hallinta.createLippu(pelaaja_id)
        return lippu1, lippu2, lippu3
    def pelaajanAloituksenLippujenValinta(self, pelaaja_id):
        lipun_hallinta = LipunHallinta()
        lippu1 = lipun_hallinta.createLippu(pelaaja_id)
        lippu2 = lipun_hallinta.createLippu(pelaaja_id)
        lippu3 = lipun_hallinta.createLippu(pelaaja_id)

        l1lahto = getIcaoFromNimi(lippu1[0])
        l1kohde = getIcaoFromNimi(lippu1[1])

        l2lahto = getIcaoFromNimi(lippu2[0])
        l2kohde = getIcaoFromNimi(lippu2[1])

        l3lahto = getIcaoFromNimi(lippu3[0])
        l3kohde = getIcaoFromNimi(lippu3[1])

        id1 = lh.getLippuId(f'{l1lahto}', f'{l1kohde}', f'{pelaaja_id}')
        id2 = lh.getLippuId(f'{l2lahto}', f'{l2kohde}', f'{pelaaja_id}')
        id3 = lh.getLippuId(f'{l3lahto}', f'{l3kohde}', f'{pelaaja_id}')

        sqlforid1 = f"select pisteet from liput inner join pelaajan_liput on id=liput_id where player_id = {pelaaja_id} and liput_id= {id1};"
        sqlforid2 = f"select pisteet from liput inner join pelaajan_liput on id=liput_id where player_id = {pelaaja_id} and liput_id= {id2};"
        sqlforid3 = f"select pisteet from liput inner join pelaajan_liput on id=liput_id where player_id = {pelaaja_id} and liput_id= {id3};"

        cursor = yhteys.cursor()
        cursor.execute(sqlforid1)
        pisteet1 = cursor.fetchone()
        cursor.execute(sqlforid2)
        pisteet2 = cursor.fetchone()
        cursor.execute(sqlforid3)
        pisteet3 = cursor.fetchone()

        print("Sinulle annetaan kolme lippua, joista sinun tulee valita 2. \nLiput jotka valitset siirtyvät sinulle.")
        print(f"Valitse ensimmäinen lippu: ")
        print(f"1. {lippu1[0]}---{lippu1[1]} ({pisteet1[0]} pistettä)\n2. {lippu2[0]}---{lippu2[1]}({pisteet2[0]} pistettä)\n3. {lippu3[0]}---{lippu3[1]}({pisteet3[0]} pistettä)")

        while True:
            try:
                syote = int(input())
                if (syote == 1):
                    valinta1 = lippu1
                    break
                elif (syote == 2):
                    valinta1 = lippu2
                    break
                elif (syote == 3):
                    valinta1 = lippu3
                    break
                else:
                    print("Virheellinen syöte!")
                    print(f"Valitse ensimmäinen lippu: ")
                    print(f"1. {lippu1[0]}---{lippu1[1]} ({pisteet1[0]} pistettä)\n2. {lippu2[0]}---{lippu2[1]}({pisteet2[0]} pistettä)\n3. {lippu3[0]}---{lippu3[1]}({pisteet3[0]} pistettä)")

                    continue
            except:
                print("Virheellinen syöte!")
                print(f"Valitse ensimmäinen lippu: ")
                print(f"1. {lippu1[0]}---{lippu1[1]} ({pisteet1[0]} pistettä)\n2. {lippu2[0]}---{lippu2[1]}({pisteet2[0]} pistettä)\n3. {lippu3[0]}---{lippu3[1]}({pisteet3[0]} pistettä)")

                continue



        print("Valitse toinen lippu: ")
        print(f"1. {lippu1[0]}---{lippu1[1]} ({pisteet1[0]} pistettä)\n2. {lippu2[0]}---{lippu2[1]}({pisteet2[0]} pistettä)\n3. {lippu3[0]}---{lippu3[1]}({pisteet3[0]} pistettä)")

        while True:
            try:
                syote = int(input())
                if (syote == 1):
                    valinta2 = lippu1
                    if (valinta2 == valinta1):
                        print("Et voi valita samaa lippua uudelleen!")
                        continue
                    else:
                        break
                elif (syote == 2):
                    valinta2 = lippu2
                    if (valinta2 == valinta1):
                        print("Et voi valita samaa lippua uudelleen!")
                        continue
                    else:
                        break
                elif (syote == 3):
                    valinta2 = lippu3
                    if (valinta2 == valinta1):
                        print("Et voi valita samaa lippua uudelleen!")
                        continue
                    else:
                        break
                else:
                    print("Virheellinen syöte!")
                    print("Valitse toinen lippu: ")
                    print(f"1. {lippu1[0]}---{lippu1[1]} ({pisteet1[0]} pistettä)\n2. {lippu2[0]}---{lippu2[1]}({pisteet2[0]} pistettä)\n3. {lippu3[0]}---{lippu3[1]}({pisteet3[0]} pistettä)")

            except:
                print("Virheellinen syöte!")
                print("Valitse toinen lippu: ")
                print(f"1. {lippu1[0]}---{lippu1[1]} ({pisteet1[0]} pistettä)\n2. {lippu2[0]}---{lippu2[1]}({pisteet2[0]} pistettä)\n3. {lippu3[0]}---{lippu3[1]}({pisteet3[0]} pistettä)")

        lippu1valittu = False
        lippu2valittu = False
        lippu3valittu = False
        liput = []

        if (lippu1==valinta1):
            lippu1valittu = True

        elif(lippu1==valinta2):
            lippu1valittu = True
        if (lippu2 == valinta1):
            lippu2valittu = True
        elif (lippu2 == valinta2):
            lippu2valittu = True
        if (lippu3 == valinta1):
            lippu3valittu=True
        elif(lippu3==valinta2):
            lippu3valittu=True

        liput.append(lippu1valittu)
        liput.append(lippu2valittu)
        liput.append(lippu3valittu)
        for i, x in enumerate(liput):
            if (i==0 and x == False):
                sqlforlahto = f"select ident from airport where name ='{lippu1[0]}';"
                sqlforkohde = f"select ident from airport where name ='{lippu1[1]}';"
                cursor = yhteys.cursor()
                cursor.execute(sqlforlahto)
                lahtolista = cursor.fetchone()
                lahto = lahtolista[0]
                cursor.execute(sqlforkohde)
                kohdelista = cursor.fetchone()
                kohde = kohdelista[0]

                sqlforid = f"select id from liput inner join pelaajan_liput on id = liput_id where lähtö = '{lahto}' and kohde = '{kohde}' and player_id = {pelaaja_id};"
                self.paivitaLokaatio(lahto, pelaaja_id)


                cursor.execute(sqlforid)
                idlist =cursor.fetchone()
                id = idlist[0]
                sql = f"delete from pelaajan_liput where liput_id={id};"
                sql2 = f"delete from liput where id = {id}"

                cursor.execute(sql)
                cursor.execute(sql2)
            elif (i==1 and x==False):
                sqlforlahto = f"select ident from airport where name ='{lippu2[0]}';"
                sqlforkohde = f"select ident from airport where name ='{lippu2[1]}';"
                cursor = yhteys.cursor()
                cursor.execute(sqlforlahto)
                lahtolista = cursor.fetchone()
                lahto = lahtolista[0]
                cursor.execute(sqlforkohde)
                kohdelista = cursor.fetchone()
                kohde = kohdelista[0]

                sqlforid = f"select id from liput inner join pelaajan_liput on id = liput_id where lähtö = '{lahto}' and kohde = '{kohde}' and player_id = {pelaaja_id};"
                self.paivitaLokaatio(lahto, pelaaja_id)

                cursor.execute(sqlforid)
                idlist = cursor.fetchone()
                id = idlist[0]
                sql = f"delete from pelaajan_liput where liput_id={id};"
                sql2 = f"delete from liput where id = {id}"
                cursor.execute(sql)
                cursor.execute(sql2)
            elif (i==2 and x==False):
                sqlforlahto = f"select ident from airport where name ='{lippu3[0]}';"
                sqlforkohde = f"select ident from airport where name ='{lippu3[1]}';"
                cursor = yhteys.cursor()
                cursor.execute(sqlforlahto)
                lahtolista = cursor.fetchone()
                lahto = lahtolista[0]
                cursor.execute(sqlforkohde)
                kohdelista = cursor.fetchone()
                kohde = kohdelista[0]

                sqlforid = f"select id from liput inner join pelaajan_liput on id = liput_id where lähtö = '{lahto}' and kohde = '{kohde}' and player_id = {pelaaja_id};"
                self.paivitaLokaatio(lahto, pelaaja_id)

                cursor.execute(sqlforid)
                idlist = cursor.fetchone()
                id = idlist[0]
                sql = f"delete from pelaajan_liput where liput_id={id};"
                sql2 = f"delete from liput where id = {id}"
                cursor.execute(sql)
                cursor.execute(sql2)

        #päivitetään pelaajan sijainti
        '''sql = f"select ident from airport where name = '{valinta1[0]}';"
        cursor = yhteys.cursor()
        cursor.execute(sql)
        tulos = cursor.fetchone()
        self.paivitaLokaatio(tulos[0], pelaaja_id)
        #return tulos[0]'''

