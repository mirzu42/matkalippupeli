from Player import *
from Lippu import *
from Kortit import *
from Reitti import *
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


#from Lentokenttienhaku import getLentokenttaNimi

kh = KortinHallinta()
ph = PelaajanHallinta()
lh = LipunHallinta()
rh = ReittiHallinta()
def deleteAll():
    rh.deleteReittiPisteet()
    kh.delete_all_kortit()
    lh.deleteLiput()
    ph.delete_all_players()
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
lh.createAloitusLiput(p_id1)
lh.createAloitusLiput(p_id2)
ph.getPelaajanLiput(p_id1)
ph.getPelaajanLiput(p_id2)
input("Paina mitä tahansa näppäintä jatkaaksesi.")
ph.getPelaajanKortit(1)
ph.getPelaajanKortit(2)
print(bcolors.WARNING+"testi")
#while True:




