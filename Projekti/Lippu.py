import mysql.connector
import geopy
from Lentokenttienhaku import laskeValimatka
yhteys = mysql.connector.connect(
         host="127.0.0.1",
         port= 3306,
         database="matkalippupeli",
         user="root",
         password="1234",
         autocommit=True
         )
class LipunHallinta():
    def createLippu(self):  # joo tää on sit ihan vitun sekava mut toimii. Jos joku keksii paremman tavan saa korjata
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

        #insert into sql
        sql3 = "select id from liput order by id asc;"
        cursor.execute(sql3)
        result5 = cursor.fetchall()

        if (len(result5)) > 0:
            lippuID = result5[-1]['id']+1
        else:
            lippuID = 1
        #pisteiden lasku
        pisteet = round(laskeValimatka(merkkijono3, merkkijono4))

        updateLahtoJaKohde = f"insert into liput (id, lähtö, kohde, pisteet) values ({lippuID}, '{merkkijono3}', '{merkkijono4}', {pisteet});"
        cursor.execute(updateLahtoJaKohde)

        return merkkijono1, merkkijono2
    def deleteLiput(self):
        sql1 = "delete from liput;"
        sql2 = "delete from pelaajan_liput;"
        cursor = yhteys.cursor()
        cursor.execute(sql1)
        cursor.execute(sql2)