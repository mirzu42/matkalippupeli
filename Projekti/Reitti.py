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

    def reittiPisteet(self, reitti_id):


