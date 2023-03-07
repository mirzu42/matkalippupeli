from Player import *
from Lippu import *
from Kortit import *
from Reitti import *
from Lentokenttienhaku import *
kh = KortinHallinta()
ph = PelaajanHallinta()
lh = LipunHallinta()
rh = ReittiHallinta()
def deleteAll():
    kh.delete_all_kortit()
    ph.delete_all_players()
    lh.deleteLiput()
    rh.deleteReittiPisteet()
    rh.deleteReitti()
#poista kaikki aikaisemmat arvot tietokannasta

deleteAll()

#main
nimi1 = input ("Syötä pelaajan 1 nimi: ")
ph.create_player(nimi1)
p_id1 = ph.getId(nimi1)
nimi2 = input("Syötä pelaajan 2 nimi: ")
ph.create_player(nimi2)
p_id2 = ph.getId(nimi2)



ph.getPelaajanKortit(1)
ph.getPelaajanKortit(2)
#while (True):






