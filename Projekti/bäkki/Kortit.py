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
class KortinHallinta():
    def createKortti(self, pelaaja_id):  #luodaan pelaajalle random kortti
        kortitLista = ["punainen", "keltainen", "sininen", "punainen", "keltainen", "sininen", "punainen", "keltainen",
                  "sininen", "jokeri"]
        kortti = random.choice(kortitLista)
        sql1 = "select id from kortit"
        cursor = yhteys.cursor()
        cursor.execute(sql1)
        result = cursor.fetchall()
        if (len(result)) > 0:
            id = result[-1][0]+1
        else:
            id = 1

        sql2 = f"insert into kortit (id, tyyppi) values ('{id}', '{kortti}');"
        cursor.execute(sql2)
        sql3 = f"insert into pelaajan_kortit (kortti_id, player_id) values ('{id}', '{pelaaja_id}');"
        cursor.execute(sql3)
    def createMultipleKortti(self, lkm, pelaaja_id):  #luodaan pelaajalle monta korttia
        for i in range(lkm):
            self.createKortti(pelaaja_id)

    def getLentokenttaKorttien_lkm(self, aport_icao):
        sql = f"select korttien_lkm from valietappi where lentokenttä_ident = '{aport_icao}'"
        cursor = yhteys.cursor()
        cursor.execute(sql)
        tulos = cursor.fetchone()
        return tulos[0]

    def delete_all_kortit(self):  #poistetaan kaikki kortit
        sql1 = f'delete from pelaajan_kortit;'
        sql2 = f"delete from kortit;"
        cursor = yhteys.cursor()
        cursor.execute(sql1)
        cursor.execute(sql2)

    def vahennaPelaajanKortteja(self, pelaaja_id, korttien_lkm):
        sql = f"update valietappi set korttien_lkm = korttien_lkm - {korttien_lkm} where player_id = '{pelaaja_id}'"
        cursor = yhteys.cursor()
        cursor.execute(sql)
        yhteys.commit()

