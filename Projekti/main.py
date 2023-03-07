from Player import *
from Lippu import *
from Kortit import *
from Reitti import *
from Lentokenttienhaku import getLentokenttaNimi
kh = KortinHallinta()
ph = PelaajanHallinta()
lh = LipunHallinta()
rh = ReittiHallinta()
def deleteAll():
    rh.deleteReittiPisteet()
    kh.delete_all_kortit()
    ph.delete_all_players()
    rh.deleteReitti()
    lh.deleteLiput()
#poista kaikki aikaisemmat arvot tietokannasta

deleteAll()

#main
nimi1 = input ("Syötä pelaajan 1 nimi: ")
ph.create_player(nimi1)
p_id1 = ph.getId(nimi1)
nimi2 = input("Syötä pelaajan 2 nimi: ")
ph.create_player(nimi2)
p_id2 = ph.getId(nimi2)
lh.createAloitusLiput(p_id1)
lh.createAloitusLiput(p_id2)


ph.getPelaajanKortit(1)
ph.getPelaajanKortit(2)
#while (True):






