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
class ReittiHallinta():
    def createReitti(self, lippu_id):
        sql1 = "select id from reitti order by id asc;"
        kursori = yhteys.cursor()
        kursori.execute(sql1)
        tulos = kursori.fetchall()

        if (len(tulos))>0:
            id = tulos[-1][0]+1
        else:
            id = 1
        sql2 = f"insert into reitti (id, lippu_id) values ({id}, {lippu_id})"
        kursori.execute(sql2)


    def reittiPisteet(self, icao, reitti_id, kortti_id, korttien_lkm, tyyppi):
        sql1 = "select id from reitti_pisteet order by id asc;"
        cursor = yhteys.cursor()
        cursor.execute(sql1)
        tulos = cursor.fetchall()

        if (len(tulos)) > 0:
            id = tulos[-1][0] + 1
        else:
            id = 1

        sql2 = f"""insert into reitti_pisteet(id, lentokenttä_ident, reitti_id, kortti_id, korttien_lkm, tyyppi)
                values ('{id}', '{icao}', '{reitti_id}', '{kortti_id}', '{korttien_lkm}', '{tyyppi}');"""
        cursor.execute(sql2)

        sql3 = f"select * from reitti_pisteet; "
        cursor.execute(sql3)
        superiortulos = cursor.fetchall()
        return superiortulos

    def haeKaikkiKentat(self):
        sql = """SELECT ident, name, latitude_deg, longitude_deg
         FROM airport
         WHERE iso_country = 'FI' 
         AND type in('medium_airport', 'large_airport')
         """
        cursor = yhteys.cursor(dictionary=True)
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

    ''' def reittiPisteetTyyppi(self):
            tyyppilista = ["sininen", "punainen", "keltainen"]
            aport_ident = self.haeKaikkiKentat()
            sql1 = "select id from reitti_pisteet order by id asc;"
            cursor = yhteys.cursor()
            cursor.execute(sql1)
            tulos = cursor.fetchall()

            if (len(tulos)) > 0:
                id = tulos[-1][0] + 1
            else:
                id = 1

            for n in aport_ident:
                tyyppi = random.choice(tyyppilista)
                icao = n['ident']
                sql2 = f"INSERT into reitti_pisteet (id, lentokenttä_ident, reitti_id, kortti_id, korttien_lkm, tyyppi) values ('{id}','{icao}', 0, 0, 3'{tyyppi}')"
                cursor = yhteys.cursor()
                cursor.execute(sql2)
    '''

    def getReittiPisteetTyyppi(self, icao):
        sql = f"select tyyppi from reitti_pisteet where lentokenttä_ident = '{icao}'"
        cursor = yhteys.cursor()
        cursor.execute(sql)
        tulos = cursor.fetchone()
        return tulos


    def deleteReitti(self):
        sql = "delete from reitti;"
        cursor = yhteys.cursor()
        cursor.execute(sql)
    def deleteReittiPisteet(self):
        sql = "delete from reitti_pisteet;"
        cursor = yhteys.cursor()
        cursor.execute(sql)

