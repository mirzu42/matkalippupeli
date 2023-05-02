import math
from geopy.distance import distance
import mysql.connector
from Reitti import *

rh = ReittiHallinta()

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

yhteys = mysql.connector.connect(
         host="mysql.metropolia.fi",
         port= 3306,
         database="lucasla",
         user="lucasla",
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

def haeLatLon(icaoKoodi):
    lat, lon = (0, 0)
    sql = "select latitude_deg, longitude_deg from airport where ident ='" + icaoKoodi + "'"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchone()
    if tulos:
        lat, lon = tulos
    return lat, lon


def laskeValimatka(icaoEka, icaoToka):
    a = haeLatLon(icaoEka)
    b = haeLatLon(icaoToka)
    return (distance(a, b)).km

#TODO
#Ei duplikaatti ilmansuuntia, sekä yksi kuuden kortin matka.

def saavutettavatLentokentat(icao):
    in_range = []
    all_ports = haeKaikkiKentat()
    for a_port in all_ports:
        dist = laskeValimatka(icao, a_port['ident'])
        korttienmaara = laskeVaadittavatKortit(dist)
        a_port['distance_kortit'] = korttienmaara
        if dist <= 374 and not dist == 0 and not dist > 374:
            in_range.append(a_port)
    in_range = sorted(in_range, key=lambda x: x['distance_kortit'])[:5]
    ilmanSuunnat(icao, in_range)
    insertKorttien_lkm(in_range)
    getReittipisteetTyyppi(in_range)
    for i in range(len(in_range)):
        print(f"{i+1}. {in_range[i]['name']}\nIlmansuunta: {in_range[i]['ilmansuunta']}\nVaadittujen korttien lukumäärä: {in_range[i]['distance_kortit']}\nVäri: {in_range[i]['tyyppi']}\n")
    return in_range


def laskeVaadittavatKortit(dist):
    max_matka = 374
    max_kortti = 6
    kortti = max_matka / max_kortti
    korttienmaara = round(dist / kortti)
    if korttienmaara < 1:
        korttienmaara = 1
    if korttienmaara > 6:
        korttienmaara = 6
    return korttienmaara

def insertKorttien_lkm(airports):
    cursor = yhteys.cursor()
    for airport in airports:
        dist = airport['distance_kortit']
        icao = airport['ident']
        sql = f"update valietappi set korttien_lkm = '{dist}' WHERE lentokenttä_ident = '{icao}'"
        cursor.execute(sql)


def getReittipisteetTyyppi(airports):
    for airport in airports:
        tyyppi = rh.getReittiPisteetTyyppi(airport['ident'])
        for i in tyyppi:
            airport['tyyppi'] = i



def ilmanSuunnat(current_aport, aports_in_range):
    current_lat, current_lon = haeLatLon(current_aport)
    compass_brackets = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    for a_port in aports_in_range:
        lat, lon = haeLatLon(a_port['ident'])
        delta_lat = lat - current_lat
        delta_lon = lon - current_lon
        radians = math.atan2(delta_lon, delta_lat)
        degrees = math.degrees(radians)
        degrees_positive = (degrees + 360) % 360
        compass_lookup = round(degrees_positive / 45) % 8
        a_port['ilmansuunta'] = compass_brackets[compass_lookup]
    return aports_in_range


def getLentokenttaNimi(icao):
    sql = f"select name from airport where ident = '{icao}'"
    cursor = yhteys.cursor()
    cursor.execute(sql)
    x = cursor.fetchone()
    return x[0]

def getIcaoFromNimi(nimi):
    sql = f"select ident from airport where name = '{nimi}'"
    cursor = yhteys.cursor()
    cursor.execute(sql)
    x = cursor.fetchone()
    return x[0]
