import math
from geopy.distance import distance
import mysql.connector

yhteys = mysql.connector.connect(
         host="127.0.0.1",
         port= 3306,
         database="matkalippupeli",
         user="root",
         password="1234",
         autocommit=True
         )

def haeKaikkiKentat():
    sql = """SELECT ident, name, latitude_deg, longitude_deg
     FROM airport
     WHERE iso_country = 'FI' 
     AND type in('medium_airport', 'large_airport')
     """
    cursor = yhteys.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def haeSijainti(icaoKoodi):
    lat, lon = (0, 0)
    sql = "select latitude_deg, longitude_deg from airport where ident ='" + icaoKoodi + "'"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchone()
    if tulos:
        lat, lon = tulos
    return lat, lon


def laskeValimatka(icaoEka, icaoToka):
    a = haeSijainti(icaoEka)
    b = haeSijainti(icaoToka)
    return (distance(a, b))


def saavutettavatLentokentät(icao, a_ports, p_range):
    in_range = []
    for a_port in a_ports:
        dist = laskeValimatka(icao, a_port['ident'])
        if dist <= p_range and not dist == 0:
            in_range.append(a_port)
    return in_range


def ilmanSuunnat(current_aport, in_range):
    current_lat, current_lon = haeSijainti(current_aport)
    compass_brackets = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    for a_port in in_range:
        lat, lon = haeSijainti(a_port['ident'])
        delta_lat = lat - current_lat
        delta_lon = lon - current_lon
        radians = math.atan2(delta_lon, delta_lat)
        degrees = math.degrees(radians)
        degrees_positive = (degrees + 360) % 360
        compass_lookup = round(degrees_positive / 45) % 8
        a_port['ilmansuunta'] = compass_brackets[compass_lookup]
    return in_range




'''def KenttienSkannaus(lentokenttä, lentokentät, lentokenttä_lat, lentokenttä_lon):
        lentokenttä_lat, lentokenttä_lon = haeSijainti(lentokenttä)
        lentokenttäetäisyys = []
        for kenttä in lentokentät:
            if kenttä != lentokenttä and kenttä in kentät:
                lat, lon = haeSijainti(kenttä)
                etäisyys = geodesic((lentokenttä_lat, lentokenttä_lon), (lat, lon)).km
                lentokenttäetäisyys.append((kenttä, etäisyys))

        Lähimmätkentät = sorted(lentokenttäetäisyys, key=lambda x: x[1])
        Lähimmätkentät = Lähimmätkentät[:5]
        return Lähimmätkentät

    kentät = haeKaikkiKentat()
    aloituslokaatio = pelaajaAloitus()
    aloituslat, aloituslon = haeSijainti(aloituslokaatio)
    lähimmätKentät = KenttienSkannaus(aloituslokaatio, kentät, aloituslat, aloituslon)
    print(lähimmätKentät) '''