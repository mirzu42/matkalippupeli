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
    def createKortti(tyyppi):
        sql1="select id from kortit;"
        cursor = yhteys.cursor()
        cursor.execute(sql1)
        result = cursor.fetchall()
        if (len(result))>0:
            id = result[-1][0]+1
        else:
            id = 1

        sql2 = f"insert into kortit (id, tyyppi) values ('{id}', '{tyyppi}');"
        cursor.execute(sql2)
        print(f"Tietokantaan listätty kortti:\nId:{id}\nTyyppi: {tyyppi}")



