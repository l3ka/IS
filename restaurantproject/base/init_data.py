# -*- encoding: utf-8 -*-
import os, sys
fileDir = os.path.dirname(os.path.abspath(__file__))
parentDir = os.path.dirname(fileDir)
sys.path.append(parentDir) 
os.environ['DJANGO_SETTINGS_MODULE'] = 'restaurantproject.settings'
import django
django.setup()

from django.contrib.auth.models import User
from django.contrib.auth.models import Group

# TODO: Alternativno import sve odjednom, nisam siguran koji pristup je bolji, pa cu dati drugima da odluce
from base.models import Sastojak
from base.models import MeniStavka
from base.models import MeniStavkaKategorija
from base.models import MeniStavkaTag
from base.models import Stol
from base.models import Konobar
from base.models import Menadzer
from base.models import Opcija
from base.models import GrupaOpcija

def addAdmin():
    User.objects.create_superuser(username='admin', email='admin@gmail.com', password='restoran')
    User.objects.create_superuser(username='admin2', email='emdepeprojektni@gmail.com', password='restoran')


# Grupe
# TODO: Moguce je korisnike same dodati u grupe, ali nisam to radio jer svejedno ne znam podesiti permisije kroz kod
# user.groups.add(grupa)
groups = []

def addGroups():
    groups.append(Group(name = "Konobari"))
    groups.append(Group(name = "Šankeri"))
    groups.append(Group(name = "Menadžeri"))
    for g in groups:
        g.save()

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
viski = MeniStavkaKategorija(redniBroj = 13, naziv = "Viski", meniStavkaKategorija = pice)

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
    viski.save()

# MeniStavka
def addMeniStavke():
    addMeniStavkaKategorija()
    jelo1 = MeniStavka(
        redniBroj = 1, 
        naziv = u"Sendvič sa sirom i voćem", 
        opis = u"Sendvič sa bogatim mediteranskim sirom i probranim voćem sa juga Grčke.",
        cijena = 8.00,
        url = "https://i.imgur.com/Tq4aP8Z.jpg",
        nijeUPonudi = False,
        meniStavkaKategorija = sendvic)
    jelo1.cache()
    jelo1.save()

    jelo2 = MeniStavka(
        redniBroj = 2,
        naziv = "Goveđi kotleti sa lukom",
        opis = "Prepoznatljiv okus o kojem ćete pričati prijateljima i porodici.",
        cijena = 9.00,
        url = "https://i.imgur.com/UEgzGXE.jpg",
        nijeUPonudi = False,
        meniStavkaKategorija = rucak
    )
    jelo2.cache()
    jelo2.save()

    jelo3 = MeniStavka(
        redniBroj = 3,
        naziv = "Odrezak u sosu sa povrćem",
        opis = "Savršen obrok za pun stomak.",
        cijena = 6.00,
        url = "https://i.imgur.com/uhbn2mu.jpg",
        nijeUPonudi = False,
        meniStavkaKategorija = dorucak
    )
    jelo3.cache()
    jelo3.save()

    jelo4 = MeniStavka(
        redniBroj = 4,
        naziv = "Dupli čizburger",
        opis = "Sadrži dvije pljeskavice.",
        cijena = 6.00,
        url = "https://i.imgur.com/UUZK3Ty.jpg",
        nijeUPonudi = False,
        meniStavkaKategorija = rucak
    )
    jelo4.cache()
    jelo4.save()

    jelo5 = MeniStavka(
        redniBroj = 5,
        naziv = "Čizburger",
        opis = "Goveđa pljeskavica.",
        cijena = 4.00,
        url = "https://i.imgur.com/MNEX5BB.jpg",
        nijeUPonudi = False,
        meniStavkaKategorija = rucak
    )
    jelo5.cache()
    jelo5.save()

    jelo6 = MeniStavka(
        redniBroj = 6,
        naziv = "Hamburger",
        opis = "Goveđa pljeskavica",
        cijena = 4.00,
        url = "https://i.imgur.com/rHuX2xQ.jpg",
        nijeUPonudi = False,
        meniStavkaKategorija = rucak
    )
    jelo6.cache()
    jelo6.save()

    jelo7 = MeniStavka(
        redniBroj = 7,
        naziv = "Johnnie Walker Blue",
        opis = "Alkoholno piće",
        cijena = 3.50,
        url = "https://i.imgur.com/Op81zst.jpg",
        nijeUPonudi = False,
        meniStavkaKategorija = viski
    )
    jelo7.cache()
    jelo7.save()

    jelo8 = MeniStavka(
        redniBroj = 8,
        naziv = "Cabernet Sauvignon",
        opis = "Autentično francusko vino.",
        cijena = 19.50,
        url = "https://i.imgur.com/zzX7kun.jpg",
        nijeUPonudi = False,
        meniStavkaKategorija = vino
    )
    jelo8.cache()
    jelo8.save()

    jelo9 = MeniStavka(
        redniBroj = 9,
        naziv = "Red Rooster Coffee",
        opis = "Kafa, tvrdo zrno.",
        cijena = 3.50,
        url = "https://i.imgur.com/PhtGe80.jpg",
        nijeUPonudi = False,
        meniStavkaKategorija = kafa
    )
    jelo9.cache()
    jelo9.save()

    # GrupaOpcija i Opcije
    # TODO: Ako neko od vas ima ideju kako da ovo napisem manje hard-coded bilo bi mega cool
    go1 = GrupaOpcija(redniBroj = 1, naziv = 'Prilog', jeIskljucivOdabir = True, jeObavezno = False, maksimalnoOdabranih = 3, meniStavka = jelo1, napomena = "")
    go1.save()
    opcijeGo1 = []
    opcijeGo1.append(Opcija(redniBroj = 1, naziv = 'Majonez', cijena = 0, imeDodatneSastojke = False, grupaOpcija = go1))
    opcijeGo1.append(Opcija(redniBroj = 2, naziv = 'Senf', cijena = 0, imeDodatneSastojke = False, grupaOpcija = go1))
    opcijeGo1.append(Opcija(redniBroj = 3, naziv = 'Urnebes', cijena = 1, imeDodatneSastojke = False, grupaOpcija = go1))
    opcijeGo1.append(Opcija(redniBroj = 4, naziv = 'Caciki sos', cijena = 0, imeDodatneSastojke = False, grupaOpcija = go1))
    opcijeGo1.append(Opcija(redniBroj = 5, naziv = 'Kajmak', cijena = 2, imeDodatneSastojke = False, grupaOpcija = go1))
    opcijeGo1.append(Opcija(redniBroj = 6, naziv = 'Pavlaka', cijena = 2, imeDodatneSastojke = False, grupaOpcija = go1))
    go1.save()
    for op in opcijeGo1:
        op.save()
    
    go2 = GrupaOpcija(redniBroj = 2, naziv = 'Prilog', jeIskljucivOdabir = True, jeObavezno = False, maksimalnoOdabranih = 3, meniStavka = jelo2, napomena = "")
    go2.save()
    opcijeGo2 = []
    opcijeGo2.append(Opcija(redniBroj = 1, naziv = 'Majonez', cijena = 0, imeDodatneSastojke = False, grupaOpcija = go2))
    opcijeGo2.append(Opcija(redniBroj = 2, naziv = 'Senf', cijena = 0, imeDodatneSastojke = False, grupaOpcija = go2))
    opcijeGo2.append(Opcija(redniBroj = 3, naziv = 'Urnebes', cijena = 1, imeDodatneSastojke = False, grupaOpcija = go2))
    opcijeGo2.append(Opcija(redniBroj = 4, naziv = 'Kajmak', cijena = 2, imeDodatneSastojke = False, grupaOpcija = go2))
    for op in opcijeGo2:
        op.save()
        
    jela = [jelo4, jelo5, jelo6]
    for index, j in enumerate(jela):
        go = GrupaOpcija(redniBroj = 3 + index, naziv = 'Prilog', jeIskljucivOdabir = True, jeObavezno = False, maksimalnoOdabranih = 3, meniStavka = j, napomena = "")
        go.save()
        opcijeGo = []
        opcijeGo.append(Opcija(redniBroj = 1, naziv = 'Majonez', cijena = 0, imeDodatneSastojke = False, grupaOpcija = go))
        opcijeGo.append(Opcija(redniBroj = 2, naziv = 'Senf', cijena = 0, imeDodatneSastojke = False, grupaOpcija = go))
        opcijeGo.append(Opcija(redniBroj = 3, naziv = 'Urnebes', cijena = 1, imeDodatneSastojke = False, grupaOpcija = go))
        opcijeGo.append(Opcija(redniBroj = 4, naziv = 'Kajmak', cijena = 2, imeDodatneSastojke = False, grupaOpcija = go))
        opcijeGo.append(Opcija(redniBroj = 5, naziv = 'Kečap', cijena = 0, imeDodatneSastojke = False, grupaOpcija = go))
        opcijeGo.append(Opcija(redniBroj = 6, naziv = 'Krastavac', cijena = 1.50, imeDodatneSastojke = False, grupaOpcija = go))
        opcijeGo.append(Opcija(redniBroj = 7, naziv = 'Paradajz', cijena = 1.50, imeDodatneSastojke = False, grupaOpcija = go))
        opcijeGo.append(Opcija(redniBroj = 8, naziv = 'Kupus salata', cijena = 0.50, imeDodatneSastojke = False, grupaOpcija = go))
        for op in opcijeGo:
            op.save()

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
addAdmin()
addGroups()
addStolovi()
addKonobari()
addMenadzeri()
addSastojke()
addMeniStavke() # addMeniStavkaKategorija() se poziva interno
addMeniStavkaTag()