import os, sys
# sys.path.append('../restaurantproject')
sys.path.append('C:/Users/Lenovo/Documents/projektniIS/is/restaurantproject')
os.environ['DJANGO_SETTINGS_MODULE'] = 'restaurantproject.settings'
import django
django.setup()

from django.contrib.auth.models import User
# TODO: Alternativno import sve odjednom, nisam siguran koji pristup je bolji, pa cu dati drugima da odluce
from users.models import Sastojak
from users.models import MeniStavka
from users.models import MeniStavkaKategorija
from users.models import MeniStavkaTag
from users.models import Stol
from users.models import Konobar
from users.models import Menadzer

# Ime, Prezime, brojSekcije, jeSefSmjene, nalog, lozinka
konobari = [
    ("Aleksije", "Mićić", 1, True, "aleksije", "restoran123"),
    ("Stefan", "Novaković", 2, True, "stefan", "restoran123"),
    ("Milorad", "Sokolović", 1, False, "milorad", "restoran123"),
    ("Nedeljko", "Milinković", 2, False, "nedeljko", "restoran123"),
]

def addKonobari():
    for konobar in konobari:
        ime, prezime, brojSekcije, jeSefSmjene, username, password = konobar
        tempUser = User.objects.create_user(username = username, password = password)
        Konobar.objects.create(ime = ime, prezime = prezime, brojSekcije = brojSekcije, jeSefSmjene = jeSefSmjene, user = tempUser)

# Ime, Prezime, nalog, lozinka
menadzeri = [
    ("Savo", "Debeljak", "savo", "restoran123"),
    ("Mihajlo", "Pavkov", "mihajlo", "stablo333"),
    ("Milan", "Pekez", "milan", "restoran123"),
    ("Darko", "Lekić", "darko", "restoran123"),
]

def addMenadzeri():
    for menadzer in menadzeri:
        ime, prezime, username, password = menadzer
        tempUser = User.objects.create_user(username = username, password = password)
        Menadzer.objects.create(ime = ime, prezime = prezime, user = tempUser)

# TODO: Remove this code?
# def addUsers():
#     for key in users.keys():
#         User.objects.create_user(username = key,password= users[key])

# MeniStavkaKategorija
jelo = MeniStavkaKategorija(redniBroj = 1, naziv = "Jelo")
pice = MeniStavkaKategorija(redniBroj = 2, naziv = "Piće")
gazirano = MeniStavkaKategorija(redniBroj = 3, naziv = "Gazirano piće", meniStavkaKategorija = pice)
negazirano = MeniStavkaKategorija(redniBroj = 4, naziv = "Negazirano piće", meniStavkaKategorija = pice)
rostilj = MeniStavkaKategorija(redniBroj = 5, naziv = "Roštilj", meniStavkaKategorija = jelo)
sendvic =  MeniStavkaKategorija(redniBroj = 6, naziv = "Sendvič", meniStavkaKategorija = jelo)
pizza =  MeniStavkaKategorija(redniBroj = 7, naziv = "Pizza", meniStavkaKategorija = jelo)
juha =  MeniStavkaKategorija(redniBroj = 8, naziv = "Juha", meniStavkaKategorija = jelo)
kafa = MeniStavkaKategorija(redniBroj = 9, naziv = "Kafa", meniStavkaKategorija = pice)
vino = MeniStavkaKategorija(redniBroj = 10, naziv = "Vino", meniStavkaKategorija = pice)
rucak = MeniStavkaKategorija(redniBroj = 11, naziv = "Ručak", meniStavkaKategorija = jelo)
dorucak = MeniStavkaKategorija(redniBroj = 12, naziv = "Doručak", meniStavkaKategorija = jelo)

def addMeniStavkaKategorija():
    jelo.save()
    pice.save()
    gazirano.save()
    negazirano.save()
    rostilj.save()
    sendvic.save()
    pizza.save() 
    juha.save()
    kafa.save()
    vino.save()
    rucak.save()
    dorucak.save()

# MeniStavka
#TODO: Popraviti da se slike ucitavaju preko relativne adrese, jer ovako ih omasi
def addMeniStavke():
    addMeniStavkaKategorija()
    jelo1 = MeniStavka(
        redniBroj = 1, 
        naziv = "Sendvič sa sirom i voćem", 
        opis = "Sendvič sa bogatim mediteranskim sirom i probranim voćem sa juga Grčke.",
        cijena = 8.00,
        fotografija = "img/d1.jpg",
        nijeUPonudi = False,
        meniStavkaKategorija = sendvic)
    jelo1.save()

    jelo2 = MeniStavka(
        redniBroj = 2,
        naziv = "Goveđi kotleti sa lukom",
        opis = "Samo najbolje goveđe meso i svježi probrani luk sa lokalne pijace daju ovom jelu čar i prepoznatljiv okus o kojem ćete pričati prijateljima i porodici.",
        cijena = 9.00,
        fotografija = "img/d2.jpg",
        nijeUPonudi = False,
        meniStavkaKategorija = rucak
    )
    jelo2.save()

    jelo3 = MeniStavka(
        redniBroj = 3,
        naziv = "Odrezak u sosu sa povrćem",
        opis = "Najkvalitetnija junetina od domaćih uzgajača, svježe probrano povrće sa lokalne pijace, vrhunski kuvari. Savršen recept za dobar provod i pun stomak.",
        cijena = 6.00,
        fotografija = "img/d3.jpg",
        nijeUPonudi = False,
        meniStavkaKategorija = dorucak
    )
    jelo3.save()

    jelo4 = MeniStavka(
        redniBroj = 4,
        naziv = "Dupli čizburger",
        opis = "Ako ste voljeli običan ili onaj dupli, sigurni smo da ćete uživati u ovoj senzaciji. Dupli čizburger ima dva komada 100% čiste govedine začinjene samo mrvicom soli i paprikom. Dostupan je sa gorkim krastavcima, seckanim lukom, kečapom, senfom i dva parčeta američkog sira. Ne sadrži veštačke ukuse, konzervanse ili dodate boje iz veštačkih izvora.",
        cijena = 6.00,
        fotografija = "img/slider1.jpg",
        nijeUPonudi = False,
        meniStavkaKategorija = rucak
    )
    jelo4.save()

# MeniStavkaTag
tagovi = [
    "slatko",
    "ljuto",
    "slano",
    "toplo",
    "ledeno",
]
def addMeniStavkaTag():
    for tag in tagovi:
        MeniStavkaTag.objects.create(tag = tag)


# Sastojak
sastojci = [
    ("Sol", False),
    ("Biber", False),
    ("Brašno", False),
    ("Origano", True),
    ("Piletina", False),
    ("Junetina", False),
    ("Soja", False),
    ("Heljdino brašno", False),
    ("Mak", False),
    ("Kurkuma", True),
    ("Čili prah", False),
    ("Paprika", False),
    ("Senf", True),
    ("Majonez", False),
    ("Kečap", True),
    ("Paradajz", False),
    ("Kupus salata", False),
    ("Kelj", False),
    ("Riža", False),
    ("Kukurz", True),
    ("Mrkva", False),
    ("Kikiriki", False),
    ("Badem", False),
]
def addSastojke():
    for sastojak in sastojci:
        naziv, jeUNedostaku = sastojak
        Sastojak.objects.create(naziv = naziv, jeUNedostaku = jeUNedostaku)

# Stol
def addStolovi():
    for brojSekcije in range(1, 4):
        for brojStola in range(1, 7):
            Stol.objects.create(brojStola = brojStola, brojSekcije = brojSekcije)


# Upustvo:
# Pozvati odgovarajucu funkciju za dodavanje te vrste objekata
# Sve je zapisano preko funkcija da ne bi imali dupliciranje (tj. prepisivanje podataka)
addSastojke()
addMeniStavke() # addMeniStavkaKategorija() se poziva interno
addMeniStavkaTag()
addStolovi()
addKonobari()
addMenadzeri()