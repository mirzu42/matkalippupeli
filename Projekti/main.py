from Player import *
from Lippu import *
from Kortit import *
from Reitti import *
from Lentokenttienhaku import *
#import keyboard

sininen =bcolors.OKBLUE
punainen = bcolors.FAIL
keltainen = bcolors.WARNING
cyan = bcolors.OKCYAN

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
rh.startingReittiPisteetTyyppi()
pelaajat = ph.getAllPelaajat()
while(True):
    nimi1 = input (sininen+"Syötä pelaajan 1 nimi: ")
    if(nimi1==""):
        print("Et voi syöttää tyhjää!")
        continue
    break


ph.create_player(nimi1)
p_id1 = ph.getId(nimi1)
while True:
    nimi2 = input (sininen+"Syötä pelaajan 2 nimi: ")
    if (nimi2.lower()==nimi1.lower()):
        print("Et voi syöttää samaa nimeä useampaan kertaan!")
        continue
    elif (nimi2 ==""):
        print("Et voi syöttää tyhjää!")
        continue
    break

ph.create_player(nimi2)
p_id2 = ph.getId(nimi2)
kh.createMultipleKortti(3,p_id1)
kh.createMultipleKortti(3,p_id2)
ph.getPelaajanLiput(p_id1)
ph.getPelaajanLiput(p_id2)
ph.getPelaajanKortit(1)
ph.getPelaajanKortit(2)
input(punainen+"Paina enter-näppäintä jatkaaksesi...")

gameover = False
while not gameover:
    print(bcolors.OKBLUE+f"Pelaaja {punainen}{ph.getNimi(p_id1)}{sininen}, mitä haluat tehdä?")
    print (f"{punainen}1) {sininen}Nostaa uuden menolipun\n{punainen}2) {sininen}Nostaa uuden kortin\n{punainen}3) {sininen}Rakentaa uuden reitin\n\n{punainen}Voit lopettaa painamalla 9\n")
    #P1 vuoro
    while True:
        try:
            syote = int(input())
            if (syote == 1):  # uuden menolipun nosto
                ph.pelaajanLipunValinta(p_id1)
                ph.getPelaajanLiput(p_id1)
                break
            elif (syote == 2):  # uuden kortin nosto
                kh.createKortti(p_id1)
                ph.getPelaajanKortit(p_id1)
                break
            elif (syote == 3):  # reitin rakennus ...öööö ei mitää käryy miten tää tehää
                print(f"{bcolors.OKBLUE}Olet " + getLentokenttaNimi(icao) + " lentokentällä")
                icao = ph.getPelaajanLokaatio(p_id1)
                ph.Liike(p_id1)
                break
            elif (syote == 9):  # lopetus
                gameover = True
                print(f"{punainen}Kiitos pelaamisesta! :)")
                break
            else:
                print(keltainen + "Virheellinen syöte!")
                continue

        except Exception as e:
            print(str(e))
            print(keltainen+"Virheellinen syöte!")
            continue

    if gameover == True:
        break
    #input("Loop ohi, toinen loop ")
    print(bcolors.OKBLUE + f"Pelaaja {punainen}{ph.getNimi(p_id2)}{sininen}, mitä haluat tehdä?")
    print(f"{punainen}1) {sininen}Nostaa uuden menolipun\n{punainen}2) {sininen}Nostaa uuden kortin\n{punainen}3) {sininen}Rakentaa uuden reitin\n\n{punainen}Voit lopettaa painamalla 9\n")
    #P2 vuoro

    while True:
        try:
            syote = int(input())
            if (syote == 1): #uuden menolipun nosto
                ph.pelaajanLipunValinta(p_id2)
                ph.getPelaajanLiput(p_id2)
                break
            elif (syote == 2): # uuden kortin nosto
                kh.createKortti(p_id2)
                ph.getPelaajanKortit(p_id2)
                break
            elif (syote == 3):  #reitin rakennus ... öööö ei mitää käryy miten tää tehää
                icao = ph.getPelaajanLokaatio(p_id2)
                print(f"{bcolors.OKBLUE}Olet " + getLentokenttaNimi(icao) + " lentokentällä")
                ph.Liike(p_id2)
                break
            elif(syote==9):
                gameover = True
                print(f"{punainen}Kiitos pelaamisesta! :)")
                break
            else:
                print(keltainen+"Virheellinen syöte!")
                continue

        except:
            print(keltainen+"Virheellinen syöte!")
            continue