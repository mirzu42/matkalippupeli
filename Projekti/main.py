from Player import *
from Lippu import *
from Kortit import *
from Reitti import *
from Lentokenttienhaku import *

ph = PelaajanHallinta()
#rh =ReittiHallinta()
#rh.createReitti(4)
#ph.uusiPelaajanKortti(1, 2)

print(ph.getId("f"))
#nimi = input("Nimi: ")
#ph.create_player(nimi)


#lista = [1,2,3,4,5,7,8,9]

kh = KortinHallinta()
#kh.createKortti(2)
#kh.createKortti(1)
ph.kaytaPelaajanKortti("punainen", 2)
#print(ph.getPuuttuva(lista, len(lista)))
#ph.kaytaMontaKorttia(2, "keltainen", 2)
#print(ph.getPelaajanKorttienLkm(2))
'''kh.delete_all_kortit()


lh = LipunHallinta()
lh.createLippu()
lh = LipunHallinta()
lh.createLippu()

#ph.uusiPelaajanKortti(2, 2)

#ph.delete_all_pelaajankortit()
#ph.delete_all_players()
'''