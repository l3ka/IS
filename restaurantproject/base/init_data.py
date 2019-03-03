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
from base.models import *

def addAdmin():
    User.objects.create_superuser(
        username='admin', email='admin@gmail.com', password='restoran')
    User.objects.create_superuser(
        username='admin2', email='admin2@gmail.com', password='restoran')


# Grupe
# TODO: Moguce je korisnike same dodati u grupe, ali nisam to radio jer svejedno ne znam podesiti permisije kroz kod
# user.groups.add(grupa)
groups = []


def addGroups():
    groups.append(Group(name="Konobari"))
    groups.append(Group(name="Šankeri"))
    groups.append(Group(name="Menadžeri"))
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
        tempUser = User.objects.create_user(
            username=username, password=password)
        Konobar.objects.create(
            ime=ime, prezime=prezime, brojSekcije=brojSekcije, jeSefSmjene=jeSefSmjene, user=tempUser)
        group = Group.objects.get(name='Konobari')
        tempUser.groups.add(group)

        if jeSefSmjene:
            group = Group.objects.get(name='Šankeri')
            tempUser.groups.add(group)


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
        tempUser = User.objects.create_user(
            username=username, password=password)
        Menadzer.objects.create(ime=ime, prezime=prezime, user=tempUser)
        group = Group.objects.get(name='Menadžeri')
        tempUser.groups.add(group)


# MeniStavkaKategorija
jelo = MeniStavkaKategorija(redniBroj=1, naziv="Jelo")
jelo.save()
pice = MeniStavkaKategorija(redniBroj=2, naziv="Piće")
pice.save()
meniStavkaKategorije = {"Gazirano piće": pice, "Negazirano piće": pice,
                        "Roštilj": jelo, "Sendvič": jelo, "Pizza": jelo, "Supa": jelo, "Kafa": pice, "Vino": pice, "Ručak": jelo, "Doručak": jelo, "Viski": pice}


def addMeniStavkaKategorija():
    for i, msk in enumerate(zip(meniStavkaKategorije.keys(), meniStavkaKategorije.values())):
        print(msk[0], msk[1])
        MeniStavkaKategorija.objects.create(redniBroj = i+3, naziv=msk[0], meniStavkaKategorija=msk[1])


# MeniStavka
# Sastojak
sastojci = [
    ("So", False),
    ("Sir", False),
    ("Voće", False),
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
    ("Pecivo", False),
    ("Govedina", False),
    ("Brokule", False)
]


def addSastojke():
    for sastojak in sastojci:
        naziv, jeUNedostaku = sastojak
        Sastojak.objects.create(naziv=naziv, jeUNedostaku=jeUNedostaku)


def addMeniStavke():
    addMeniStavkaKategorija()
    sendvic = MeniStavka(
        redniBroj=1,
        naziv=u"Sendvič sa sirom i voćem",
        opis=u"Sendvič sa bogatim mediteranskim sirom i probranim voćem sa juga Grčke.",
        cijena=8.00,
        url="https://i.imgur.com/Tq4aP8Z.jpg",
        nijeUPonudi=False,
        meniStavkaKategorija=MeniStavkaKategorija.objects.filter(naziv='Sendvič').first()
    )

    sendvic.cache()
    sendvic.save()

    SastojakMeniStavka(kolicina='5g', sastojak=Sastojak.objects.filter(
        naziv="So").first(), meniStavka=sendvic).save()
    SastojakMeniStavka(kolicina='40g', sastojak=Sastojak.objects.filter(
        naziv="Sir").first(), meniStavka=sendvic).save()
    SastojakMeniStavka(kolicina='60g', sastojak=Sastojak.objects.filter(
        naziv="Voće").first(), meniStavka=sendvic).save()
    SastojakMeniStavka(kolicina='60g', sastojak=Sastojak.objects.filter(
        naziv="Origano").first(), meniStavka=sendvic).save()
    SastojakMeniStavka(kolicina='150g', sastojak=Sastojak.objects.filter(
        naziv="Pecivo").first(), meniStavka=sendvic).save()

    govedina = MeniStavka(
        redniBroj=2,
        naziv="Goveđi kotleti sa lukom",
        opis="Samo najbolje goveđe meso i svježi probrani luk sa lokalne pijace daju ovom jelu čar i prepoznatljiv okus o kojem ćete pričati prijateljima i porodici.",
        cijena=19.00,
        url="https://i.imgur.com/UEgzGXE.jpg",
        nijeUPonudi=False,
        meniStavkaKategorija=MeniStavkaKategorija.objects.filter(naziv='Ručak').first()
    )

    govedina.cache()
    govedina.save()
    SastojakMeniStavka(kolicina='10g', sastojak=Sastojak.objects.filter(
        naziv="So").first(), meniStavka=govedina).save()
    SastojakMeniStavka(kolicina='20g', sastojak=Sastojak.objects.filter(
        naziv="Sir").first(), meniStavka=govedina).save()
    SastojakMeniStavka(kolicina='250g', sastojak=Sastojak.objects.filter(
        naziv="Govedina").first(), meniStavka=govedina).save()
    SastojakMeniStavka(kolicina='2g', sastojak=Sastojak.objects.filter(
        naziv="Biber").first(), meniStavka=govedina).save()
    SastojakMeniStavka(kolicina='70g', sastojak=Sastojak.objects.filter(
        naziv="Brokule").first(), meniStavka=govedina).save()


    odrezak = MeniStavka(
        redniBroj=3,
        naziv="Odrezak u sosu sa povrćem",
        opis="Najkvalitetnija junetina od domaćih uzgajača, svježe probrano povrće sa lokalne pijace, vrhunski kuvari. Savršen recept za dobar provod i pun stomak.",
        cijena=16.00,
        url="https://i.imgur.com/uhbn2mu.jpg",
        nijeUPonudi=False,
        meniStavkaKategorija=MeniStavkaKategorija.objects.filter(naziv='Doručak').first()
    )
    odrezak.cache()
    odrezak.save()
    SastojakMeniStavka(kolicina='10g', sastojak=Sastojak.objects.filter(
        naziv="So").first(), meniStavka=odrezak).save()
    SastojakMeniStavka(kolicina='50g', sastojak=Sastojak.objects.filter(
        naziv="Brokule").first(), meniStavka=odrezak).save()
    SastojakMeniStavka(kolicina='250g', sastojak=Sastojak.objects.filter(
        naziv="Junetina").first(), meniStavka=odrezak).save()
    SastojakMeniStavka(kolicina='2g', sastojak=Sastojak.objects.filter(
        naziv="Biber").first(), meniStavka=odrezak).save()
    SastojakMeniStavka(kolicina='70g', sastojak=Sastojak.objects.filter(
        naziv="Mrkva").first(), meniStavka=odrezak).save()

    duplicizburger = MeniStavka(
        redniBroj=4,
        naziv="Dupli čizburger",
        opis="Ako ste voljeli običan ili onaj dupli, sigurni smo da ćete uživati u ovoj senzaciji. Dupli čizburger ima dva komada 100% čiste govedine začinjene samo mrvicom soli i paprikom. Dostupan je sa gorkim krastavcima, seckanim lukom, kečapom, senfom i dva parčeta američkog sira. Ne sadrži veštačke ukuse, konzervanse ili dodate boje iz veštačkih izvora.",
        cijena=6.00,
        url="https://i.imgur.com/UUZK3Ty.jpg",
        nijeUPonudi=False,
        meniStavkaKategorija=MeniStavkaKategorija.objects.filter(naziv='Ručak').first()
    )
    duplicizburger.cache()
    duplicizburger.save()

    SastojakMeniStavka(kolicina='10g', sastojak=Sastojak.objects.filter(
        naziv="So").first(), meniStavka=duplicizburger).save()
    SastojakMeniStavka(kolicina='100g', sastojak=Sastojak.objects.filter(
        naziv="Govedina").first(), meniStavka=duplicizburger).save()
    SastojakMeniStavka(kolicina='20g', sastojak=Sastojak.objects.filter(
        naziv="Sir").first(), meniStavka=duplicizburger).save()


    cizburger = MeniStavka(
        redniBroj=5,
        naziv="Čizburger",
        opis="Čizburger ima komad 100% čiste govedine začinjene samo mrvicom soli i paprikom. Dostupan je sa gorkim krastavcima, seckanim lukom, kečapom, senfom i parčetom američkog sira. Ne sadrži veštačke ukuse, konzervanse ili dodate boje iz veštačkih izvora.",
        cijena=4.00,
        url="https://usateatsiptrip.files.wordpress.com/2018/08/gettyimages-589115286.jpg?w=1024&h=615&crop=1",
        nijeUPonudi=False,
        meniStavkaKategorija=MeniStavkaKategorija.objects.filter(naziv='Ručak').first()
    )

    cizburger.cache()
    cizburger.save()
    SastojakMeniStavka(kolicina='10g', sastojak=Sastojak.objects.filter(
        naziv="So").first(), meniStavka=cizburger).save()
    SastojakMeniStavka(kolicina='50g', sastojak=Sastojak.objects.filter(
        naziv="Govedina").first(), meniStavka=cizburger).save()
    SastojakMeniStavka(kolicina='10g', sastojak=Sastojak.objects.filter(
        naziv="Sir").first(), meniStavka=cizburger).save()


    hamburger = MeniStavka(
        redniBroj=6,
        naziv="Hamburger",
        opis="Hamburger ima komad 100% čiste govedine začinjene samo mrvicom soli i paprikom. Dostupan je sa gorkim krastavcima, seckanim lukom, kečapom i senfom. Ne sadrži veštačke ukuse, konzervanse ili dodate boje iz veštačkih izvora.",
        cijena=4.00,
        url="https://i.imgur.com/rHuX2xQ.jpg",
        nijeUPonudi=False,
        meniStavkaKategorija=MeniStavkaKategorija.objects.filter(naziv='Ručak').first()
    )
    hamburger.cache()
    hamburger.save()
    SastojakMeniStavka(kolicina='10g', sastojak=Sastojak.objects.filter(
        naziv="So").first(), meniStavka=hamburger).save()
    SastojakMeniStavka(kolicina='70g', sastojak=Sastojak.objects.filter(
        naziv="Govedina").first(), meniStavka=hamburger).save()


    johnie = MeniStavka(
        redniBroj=7,
        naziv="Johnnie Walker Blue",
        opis="Dok nas nijedna druga boja Johnnie Walker-a ne oduševljava, svaki ima malo elemenata koje nas slučajno oduševe. Ovi dobri elementi udružuju snage kako bi stvorili Johnnie Valker Blue. To je kao Voltron. Johnnie Walker Blue je žvakljiv i gladak sa balansom od karamela, dima i zemljanih tonova, što znači da je Johnnie Valker samo želeo da podeli najbolje što je imao da ponudi. To nije najbolji scotch kojeg smo ikada imali, ali to je \"veliki\" škotski štok, kojeg čak i ljudi koji ne piju znaju.",
        cijena=3.50,
        url="https://i.imgur.com/Op81zst.jpg",
        nijeUPonudi=False,
        meniStavkaKategorija=MeniStavkaKategorija.objects.filter(naziv='Viski').first()
    )
    johnie.cache()
    johnie.save()

    sauvignon = MeniStavka(
        redniBroj=8,
        naziv="Cabernet Sauvignon",
        opis="2014 Cabernet Sauvignon Mayacamas vinograda je graciozan povratak u obliku iz ikone Napa vinarije. Promene u vlasništvu, građanski sporovi i brige o odlasku iz tradicionalnog, elegantnog stila vinarije postaju daleke uspomene prilikom ukusa ovog moćnog ali fokusiranog vina. Veoma lagan hrastov uticaj dozvoljava da sjajni, sunčano natopljen karakter Mount Veeder-a. Kiselost je sjajna, a vino ima kiselog, sočnog crnog voća. Bilje i crni slatki korijen dodaju nijansu, dok su žvakani tanini uporni u trajnom završetku, koji je bogat kamenim mineralnim notama. Ako su vam prekomerno izduvani Napa Cabs okrenuli daleko od sorte i regije, ova boca obećava da vas vraća unazad. Vintage izuzetno dobro pije, ali je i dalje beba. Ovo vino sazreće sa milosrćnošću i elegancijom i može se ostaviti u podrumu decenijama.",
        cijena=19.50,
        url="https://i.imgur.com/zzX7kun.jpg",
        nijeUPonudi=False,
        meniStavkaKategorija=MeniStavkaKategorija.objects.filter(naziv='Vino').first()
    )
    sauvignon.cache()
    sauvignon.save()

    coffee = MeniStavka(
        redniBroj=9,
        naziv="Red Rooster Coffee",
        opis="Uravnoteženo, bogato slatko, tarto i ukusno. Fini mošus, osušeni cvet hibiskusa, perik (fermentirani) sušeni duvan, pečurke i šampinjone, aroma kajsije. Slatko-tart-ukusna struktura s pikantnom kiselinom; lagano kremasto, nezasitan okus. Bogato tonirana završna obrada oko marelica i odiše umami note slične gljivicama sa šampinjonima.",
        cijena=3.50,
        url="https://i.imgur.com/PhtGe80.jpg",
        nijeUPonudi=False,
        meniStavkaKategorija=MeniStavkaKategorija.objects.filter(naziv='Kafa').first()
    )
    coffee.cache()
    coffee.save()

    # GrupaOpcija i Opcije
    # TODO: Ako neko od vas ima ideju kako da ovo napisem manje hard-coded bilo bi mega cool
    go1 = GrupaOpcija(redniBroj=1, naziv='Prilog', jeIskljucivOdabir=True,
                      jeObavezno=False, maksimalnoOdabranih=3, meniStavka=sendvic, napomena="")
    go1.save()
    opcijeGo1 = []
    opcijeGo1.append(Opcija(redniBroj=1, naziv='Majonez',
                            cijena=0, imaDodatneSastojke=False, grupaOpcija=go1))
    opcijeGo1.append(Opcija(redniBroj=2, naziv='Senf', cijena=0,
                            imaDodatneSastojke=False, grupaOpcija=go1))
    opcijeGo1.append(Opcija(redniBroj=3, naziv='Urnebes',
                            cijena=1, imaDodatneSastojke=False, grupaOpcija=go1))
    opcijeGo1.append(Opcija(redniBroj=4, naziv='Caciki sos',
                            cijena=0, imaDodatneSastojke=False, grupaOpcija=go1))
    opcijeGo1.append(Opcija(redniBroj=5, naziv='Kajmak',
                            cijena=2, imaDodatneSastojke=False, grupaOpcija=go1))
    opcijeGo1.append(Opcija(redniBroj=6, naziv='Pavlaka',
                            cijena=2, imaDodatneSastojke=False, grupaOpcija=go1))

    for op in opcijeGo1:
        op.save()

    go2 = GrupaOpcija(redniBroj=2, naziv='Prilog', jeIskljucivOdabir=True,
                      jeObavezno=False, maksimalnoOdabranih=3, meniStavka=govedina, napomena="")
    go2.save()
    opcijeGo2 = []
    opcijeGo2.append(Opcija(redniBroj=1, naziv='Majonez',
                            cijena=0, imaDodatneSastojke=False, grupaOpcija=go2))
    opcijeGo2.append(Opcija(redniBroj=2, naziv='Senf', cijena=0,
                            imaDodatneSastojke=False, grupaOpcija=go2))
    opcijeGo2.append(Opcija(redniBroj=3, naziv='Urnebes',
                            cijena=1, imaDodatneSastojke=False, grupaOpcija=go2))
    opcijeGo2.append(Opcija(redniBroj=4, naziv='Kajmak',
                            cijena=2, imaDodatneSastojke=False, grupaOpcija=go2))
    for op in opcijeGo2:
        op.save()

    jela = [duplicizburger, cizburger, hamburger]
    for index, j in enumerate(jela):
        go = GrupaOpcija(redniBroj=3 + index, naziv='Prilog', jeIskljucivOdabir=True,
                         jeObavezno=False, maksimalnoOdabranih=3, meniStavka=j, napomena="")
        go.save()
        opcijeGo = []
        opcijeGo.append(Opcija(redniBroj=1, naziv='Majonez',
                               cijena=0, imaDodatneSastojke=False, grupaOpcija=go))
        opcijeGo.append(Opcija(redniBroj=2, naziv='Senf', cijena=0,
                               imaDodatneSastojke=False, grupaOpcija=go))
        opcijeGo.append(Opcija(redniBroj=3, naziv='Urnebes',
                               cijena=1, imaDodatneSastojke=False, grupaOpcija=go))
        opcijeGo.append(Opcija(redniBroj=4, naziv='Kajmak',
                               cijena=2, imaDodatneSastojke=False, grupaOpcija=go))
        opcijeGo.append(Opcija(redniBroj=5, naziv='Kečap',
                               cijena=0, imaDodatneSastojke=False, grupaOpcija=go))
        opcijeGo.append(Opcija(redniBroj=6, naziv='Krastavac',
                               cijena=1.50, imaDodatneSastojke=False, grupaOpcija=go))
        opcijeGo.append(Opcija(redniBroj=7, naziv='Paradajz',
                               cijena=1.50, imaDodatneSastojke=False, grupaOpcija=go))
        opcijeGo.append(Opcija(redniBroj=8, naziv='Kupus salata',
                               cijena=0.50, imaDodatneSastojke=False, grupaOpcija=go))
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
        MeniStavkaTag.objects.create(tag=tag)

# Stol


def addStolovi():
    for brojSekcije in range(3):
        for k in range(1,7):
            Stol.objects.create(brojStola=brojSekcije*6 + k, brojSekcije=brojSekcije + 1)


# Upustvo:
# Pozvati odgovarajucu funkciju za dodavanje te vrste objekata
# Sve je zapisano preko funkcija da ne bi imali dupliciranje (tj. prepisivanje podataka)
addAdmin()
addGroups()
addStolovi()
addKonobari()
addMenadzeri()
addSastojke()
addMeniStavke()  # addMeniStavkaKategorija() se poziva interno
addMeniStavkaTag()