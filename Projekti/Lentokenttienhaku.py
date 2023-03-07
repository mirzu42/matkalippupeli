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
    return (distance(a, b)).km


def saavutettavatLentokentat(icao, p_range):
    max_matka = 374
    max_kortti = 6
    in_range = []
    all_ports = haeKaikkiKentat()
    for a_port in all_ports:
        dist = laskeValimatka(icao, a_port['ident'])
        kortti = max_matka / max_kortti
        korttienmaara = round(dist / kortti)
        if korttienmaara < 1:
            korttienmaara = 1
        if korttienmaara > 6:
            korttienmaara = 6
        a_port['distance_kortit'] = korttienmaara
        if dist <= p_range and not dist == 0 and not dist > 374:
            in_range.append(a_port)
    in_range = sorted(in_range, key=lambda x: x['distance_kortit'])[:5]
    return in_range, korttienmaara


def ilmanSuunnat(current_aport, aport_in_range):
    current_lat, current_lon = haeSijainti(current_aport)
    compass_brackets = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    for a_port in aport_in_range:
        lat, lon = haeSijainti(a_port['ident'])
        delta_lat = lat - current_lat
        delta_lon = lon - current_lon
        radians = math.atan2(delta_lon, delta_lat)
        degrees = math.degrees(radians)
        degrees_positive = (degrees + 360) % 360
        compass_lookup = round(degrees_positive / 45) % 8
        a_port['ilmansuunta'] = compass_brackets[compass_lookup]
    return aport_in_range




'''current_aport = "EFHK"
all_aports = haeKaikkiKentat()
p_range = 400
# Call the function
in_range = saavutettavatLentokentat(current_aport, p_range)
#testi = ilmanSuunnat(current_aport, in_range)
print(in_range)'''
