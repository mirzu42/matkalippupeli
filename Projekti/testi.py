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
kh = KortinHallinta()
ph = PelaajanHallinta()
lh = LipunHallinta()
rh = ReittiHallinta()

#lh.createLippu(2)
#ph.getPelaajanLiput(2)
ph.Liike(4)
#print(kh.getKorttien_lkm("EFHk"))