import mysql.connector
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
        lahto = "select name from airport where iso_country = 'fi' and type in('medium_airport', 'large_airport') order by rand() limit 1"
        cursor.execute(lahto)
        result1 = cursor.fetchall()
        kohde = "select name from airport where iso_country = 'fi' and type in('medium_airport', 'large_airport') order by rand() limit 1"
        cursor.execute(kohde)
        result2 = cursor.fetchall()
        if result2 == result1:
            kohde = "select name from airport where iso_country = 'fi' and type in('medium_airport', 'large_airport') order by rand() limit 1"
            cursor.execute(kohde)
            result2 = cursor.fetchall()
        merkkijono1 = ''.join(str(x) for x in result1)
        merkkijono2 = ''.join(str(y) for y in result2)
        sql1 = f"select ident from airport where name = '{merkkijono1[10:-2]}'"
        cursor.execute(sql1)
        result3 = cursor.fetchall()
        sql2 = f"select ident from airport where name = '{merkkijono2[10:-2]}'"
        cursor.execute(sql2)
        result4 = cursor.fetchall()
        merkkijono3 = ''.join(str(x) for x in result3)
        merkkijono4 = ''.join(str(x) for x in result4)

        #insert into sql
        sql3 = "select id from liput order by id asc;"
        cursor.execute(sql3)
        result5 = cursor.fetchall()

        if (len(result5)) > 0:
            lippuID = result5[-1]['id']+1
            print(lippuID)
        else:
            lippuID = 1
            print(lippuID)

        print(merkkijono3[11:-2])
        print(merkkijono4[11:-2])
        updateLahtoJaKohde = f"insert into liput (id, lähtö, kohde, pisteet) values ({lippuID}, '{merkkijono3[11:-2]}', '{merkkijono4[11:-2]}', 40);"
        cursor.execute(updateLahtoJaKohde)

        return merkkijono1[10:-2], merkkijono2[10:-2]