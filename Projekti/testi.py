import mysql.connector
from Player import *
from Lippu import *
from Kortit import *
from Reitti import *
from Lentokenttienhaku import getLentokenttaNimi
from Lentokenttienhaku import *
yhteys = mysql.connector.connect(
         host="127.0.0.1",
         port= 3306,
         database="matkalippupeli",
         user="root",
         password="1234",
         autocommit=True
         )
ph = PelaajanHallinta()
ph.pelaajanAloituksenLippujenValinta(3)