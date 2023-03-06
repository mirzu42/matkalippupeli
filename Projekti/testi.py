import mysql.connector
yhteys = mysql.connector.connect(
         host="127.0.0.1",
         port= 3306,
         database="matkalippupeli",
         user="root",
         password="1234",
         autocommit=True
         )
lahto, kohde = 0, 1
i = 0
while lahto != kohde:
    sql = "select name from airport where iso_country = 'fi' and type in('medium_airport', 'large_airport') order by rand() limit 2"
    cursor = yhteys.cursor(dictionary=True)
    cursor.execute(sql)
    tulos = cursor.fetchall()
    lahto, kohde = tulos
    print(lahto, kohde)
    if lahto == kohde:
        print("2 samaa")
        break