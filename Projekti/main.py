from Player import *
from Lippu import *
from Kortit import *
from Reitti import *
from Lentokenttienhaku import *

ph = PelaajanHallinta()
#rh =ReittiHallinta()
#rh.createReitti(4)
#ph.uusiPelaajanKortti(1, 2)


nimi = input("Nimi: ")
ph.create_player(nimi)



kh = KortinHallinta()
kh.createKortti(1)
kh.delete_all_kortit()
lh = LipunHallinta()
lh.createLippu()

#kh = KortinHallinta
#kh.createKortti("Punainen")

#ph.uusiPelaajanKortti(2, 2)


#ph.delete_all_pelaajankortit()
#ph.delete_all_players()
