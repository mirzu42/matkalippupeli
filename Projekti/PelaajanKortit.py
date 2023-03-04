import mysql.connector

yhteys = mysql.connector.connect(
         host="127.0.0.1",
         port= 3306,
         database="matkalippupeli",
         user="root",
         password="1234",
         autocommit=True
         )
class PelaajanKorttienHallinta():
    def uusiPelaajanKortti(pelaaja_id, kortti_id):
        sql = f"insert into pelaajan_kortit (kortti_id, player_id) values ({pelaaja_id}, {kortti_id})"
        cursor = yhteys.cursor()
        cursor.execute(sql)
        print (f"Tietokantaan lisätty pelaajan kortti: kortti_id: {kortti_id}\npelaaja_id: {pelaaja_id}")
