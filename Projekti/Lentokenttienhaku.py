from geopy.distance import distance
import mysql.connector
yhteys = mysql.connector.connect(
         host="127.0.0.1",
         port= 3306,
         database="flight_game",
         user="root",
         password="root1234",
         autocommit=True
         )

def haeKaikkiKentat():
    kentät = []
    sql = "select airport.ident from airport inner join country on airport.iso_country = country.iso_country where country.name = 'Finland' and type != 'closed' and type !='heliport' and type !='small_airport';"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchall()
    if (kursori.rowcount>0):
        for rivi in tulos:
            kentät.append(rivi[0])
    return kentät
def haeSijainti(icaoKoodi):
    lat, lon =(0,0)
    sql = "select ident, latitude_deg, longitude_deg from airport where ident ='"+icaoKoodi+"'"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchall()
    if (kursori.rowcount>0):
        for rivi in tulos:
            lat=rivi[1]
            lon=rivi[2]
    return lat, lon

def laskeValimatka(icaoEka, icaoToka):
    latitudeOne = haeSijainti(icaoEka)[0]
    longitudeOne = haeSijainti(icaoEka)[1]
    latitudeTwo = haeSijainti(icaoToka)[0]
    longitudeTwo = haeSijainti(icaoToka)[1]
    a = latitudeOne, longitudeOne
    b = latitudeTwo, longitudeTwo
    print(distance(a, b))

kentät = haeKaikkiKentat()


