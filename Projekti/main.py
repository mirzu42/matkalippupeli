from Player import *
from Lippu import *
from Kortit import *
from PelaajanKortit import*
from Lentokenttienhaku import *

ph = PelaajanHallinta()
pkh = PelaajanKorttienHallinta


nimi = input("Nimi: ")
ph.create_player(nimi)

lh = LipunHallinta()
lh.createLippu()
print(ph.pelaajaAloitus())

kh = KortinHallinta
kh.createKortti("Punainen")
lh = LipunHallinta()
lh.createLippu()
kh = KortinHallinta
kh.createKortti("Punainen")

ph.uusiPelaajanKortti(1, 1)


#pkh.delete_all_pelaajankortit("")
#ph.delete_all_players()
