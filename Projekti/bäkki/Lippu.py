import mysql.connector
import geopy
from Lentokenttienhaku import laskeValimatka

yhteys = mysql.connector.connect(
     host="mysql.metropolia.fi",
     port= 3306,
     database="lucasla",
     user="lucasla",
     password="1234",
     autocommit=True
     )
class LipunHallinta():
    def createLippu(self, p_id):  #luodaan pelaajalle menolippu suomessa olevista isoista ja keskikokoisista lentokentistä
        cursor = yhteys.cursor(dictionary=True)
        sql = "select name from airport where iso_country = 'fi' and type in('medium_airport', 'large_airport') order by rand() limit 2"
        cursor.execute(sql)
        result = cursor.fetchall()
        result1, result2 = result
        merkkijono1 = result1['name']
        merkkijono2 = result2['name']
        sql1 = f"select ident from airport where name = '{merkkijono1}'"
        cursor.execute(sql1)
        result3 = cursor.fetchone()
        sql2 = f"select ident from airport where name = '{merkkijono2}'"
        cursor.execute(sql2)
        result4 = cursor.fetchone()
        merkkijono3 = result3['ident']
        merkkijono4 = result4['ident']

        sql3 = "select id from liput order by id asc;"
        cursor.execute(sql3)
        result5 = cursor.fetchall()

        if (len(result5)) > 0:
            lippuID = result5[-1]['id']+1
        else:
            lippuID = 1
        #pisteiden lasku
        pisteet = round(laskeValimatka(merkkijono3, merkkijono4))

        #insert into sql
        updateLahtoJaKohde = f"insert into liput (id, lähtö, kohde, pisteet) values ({lippuID}, '{merkkijono3}', '{merkkijono4}', {pisteet});"
        cursor.execute(updateLahtoJaKohde)

        #Lisätään lippu pelaajalle
        sql4 = f"insert into pelaajan_liput (player_id, liput_id) values ({p_id}, {lippuID})"
        cursor.execute(sql4)

        return merkkijono1, merkkijono2, pisteet, merkkijono3


    def getAloitusLipunIcao(self, p_id):
        for i in range(3):
            self.createLippu(p_id)
        sql = f"select lähtö, kohde from liput inner join pelaajan_liput on id=liput_id where player_id = '{p_id}'"
        cursor = yhteys.cursor()
        cursor.execute(sql)
        tulos = cursor.fetchall()
        return tulos

    def deleteLiput(self):  #poistaa kaikki pelaajan liput
        sql1 = "delete from pelaajan_liput;"
        sql2 = "delete from liput;"
        cursor = yhteys.cursor()
        cursor.execute(sql1)
        cursor.execute(sql2)
    '''def createAloitusLiput(self, p_id):  #luo pelaajalle 3 lippua
        for i in range(3):
            self.createLippu(p_id)'''
    def getLippuId(self, lahto, kohde, p_id):
        getid = f"select id from liput inner join pelaajan_liput on id = liput_id where kohde = '{kohde}' and lähtö ='{lahto}' and player_id = {p_id};"
        cursor = yhteys.cursor()
        cursor.execute(getid)
        tulos = cursor.fetchone()
        return tulos[0]

