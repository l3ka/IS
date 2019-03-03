from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.files import File
import urllib.request
import os

class Dogadjaj(models.Model):
    naziv = models.CharField(max_length = 20, help_text = 'Unesite naziv događaja')
    opis = models.TextField()
    datumVrijeme = models.DateTimeField()
    fotografija = models.ImageField(upload_to = 'photos/dogadjaji/%Y/%m/%d')

    def __str__(self):
        return self.naziv

class Promocija(models.Model):
    naziv = models.CharField(max_length = 20, help_text = 'Unesite naziv promocije')
    vaziOd = models.DateTimeField()
    vaziDo = models.DateTimeField()
    dogadjaj = models.ForeignKey(Dogadjaj, on_delete=models.CASCADE)

    def __str__(self):
        return self.naziv

class Stol(models.Model):
    brojStola = models.IntegerField()
    brojSekcije = models.IntegerField()

    def __str__(self):
        return f'Stol {self.brojSekcije}.{self.brojStola}'

class Menadzer(models.Model):
    ime = models.CharField(max_length = 20, help_text = 'Unesite svoje ime')
    prezime = models.CharField(max_length = 20, help_text = 'Unesite svoje prezime')
    user = models.OneToOneField(User, on_delete = models.PROTECT)

    def __str__(self):
        return f'{self.ime} {self.prezime}'

class Konobar(models.Model):
    ime = models.CharField(max_length = 20, help_text = 'Unesite svoje ime')
    prezime = models.CharField(max_length = 20, help_text = 'Unesite svoje prezime')
    brojSekcije = models.IntegerField()
    jeSefSmjene = models.BooleanField()
    user = models.OneToOneField(User, on_delete = models.PROTECT)

    def __str__(self):
        return f'{self.ime} {self.prezime}'

class Sastojak(models.Model):
    naziv = models.CharField(max_length = 20, help_text = 'Unesite naziv sastojka')
    jeUNedostaku = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.naziv

class MeniStavka(models.Model):
    redniBroj = models.IntegerField()
    naziv = naziv = models.CharField(max_length = 30, help_text = 'Unesite naziv stavke')
    opis = models.TextField()
    cijena = models.DecimalField(max_digits = 4, decimal_places = 2)
    url = models.CharField(max_length = 255, unique = True)
    fotografija = models.ImageField(upload_to = 'photos/menu/%Y/%m/%d', blank = True)
    nijeUPonudi = models.BooleanField()
    meniStavkaKategorija = models.ForeignKey('MeniStavkaKategorija', on_delete = models.PROTECT)

    def __str__(self):
        return self.naziv

    def cache(self):
        if self.url and not self.fotografija:
            result = urllib.request.urlretrieve(self.url)
            self.fotografija.save(
                    os.path.basename(self.url),
                    File(open(result[0], 'rb'))
                    )
            self.save()

class MeniStavkaTag(models.Model):
    tag = models.CharField(max_length = 20, help_text = 'Unesite tag')

    def __str__(self):
        return self.tag

class SastojakMeniStavka(models.Model):
   kolicina = models.CharField(max_length=20, help_text='Unesite kolicinu')
   sastojak = models.ForeignKey(Sastojak, on_delete = models.PROTECT) 
   meniStavka = models.ForeignKey(MeniStavka, on_delete = models.PROTECT)

class GrupaOpcija(models.Model):
    redniBroj = models.IntegerField()
    naziv = models.CharField(max_length = 20, help_text = 'Unesite naziv grupe opcije')
    jeIskljucivOdabir = models.BooleanField()
    jeObavezno = models.BooleanField()
    maksimalnoOdabranih = models.IntegerField()
    napomena = models.TextField()
    meniStavka = models.ForeignKey(MeniStavka, on_delete = models.CASCADE)

    def __str__(self):
        return f'{self.naziv} - {self.meniStavka}'

class Opcija(models.Model):
    redniBroj = models.IntegerField()
    naziv = models.CharField(max_length = 20, help_text = 'Unesite naziv opcije')
    cijena = models.DecimalField(max_digits = 6, decimal_places = 2)
    imaDodatneSastojke = models.BooleanField()
    grupaOpcija = models.ForeignKey(GrupaOpcija, on_delete = models.CASCADE)

    def __str__(self):
        return f'{self.naziv} - {self.grupaOpcija}'

class OpcijaSastojak(models.Model):
    sastojak = models.ForeignKey(Sastojak, on_delete = models.PROTECT)
    opcija = models.ForeignKey(Opcija, on_delete = models.PROTECT)

class PromotivnaCijena(models.Model):
    cijena = models.DecimalField(max_digits = 4, decimal_places = 2)
    meniStavka = models.ForeignKey(MeniStavka, on_delete = models.CASCADE)
    promocija = models.ForeignKey(Promocija, on_delete = models.CASCADE)

class MeniStavkaKategorija(models.Model):
    redniBroj = models.IntegerField()
    naziv = models.CharField(max_length = 20, help_text = 'Unesite naziv')
    meniStavkaKategorija = models.ForeignKey('self', on_delete = models.CASCADE,blank=True,null=True) # TODO: PRODISKUTOVATI on_delete

    def __str__(self):
        return self.naziv

class MeniStavkaKategorijaTag(models.Model):
    tag = models.CharField(max_length = 32, help_text = 'Unesite tag')
    meniStavkaKategorijaTag = models.ForeignKey(MeniStavkaKategorija, on_delete = models.PROTECT)

class Narudzba(models.Model):
    vrijemeKreiranja = models.DateTimeField(default=timezone.now)
    vrijemeProcesiranja = models.DateTimeField(blank=True, null=True)
    status = models.TextField(default="AWAITING_PROCESSING")
    jePrihvacena = models.BooleanField(default=False)
    napomena = models.TextField(blank=True, null=True)
    razlogOdbijanja = models.TextField(blank=True, null=True)
    dojam = models.TextField(blank=True, null=True)
    stol = models.IntegerField(blank=True, null=True)
    # TODO: Napraviti da radi i objasniti zasto ne radi?
    konobarProcesira = models.ForeignKey(Konobar, on_delete = models.PROTECT, related_name = 'konobar_procesirao', null = True, blank=True)
    konobarKreira = models.ForeignKey(Konobar, on_delete = models.PROTECT, related_name = 'konobar_kreirao', null = True, blank=True)
    pushEndpoint = models.TextField(blank=True, null=True)
    def __str__(self):
        return f'Narudbza {self.id}'
    
class NarudzbaStavka(models.Model):
    redniBroj = models.IntegerField()
    cijenaBezOpcija = models.DecimalField(max_digits = 6, decimal_places = 2)
    kolicina = models.IntegerField()
    napomena = models.TextField()
    meniStavka = models.ForeignKey(MeniStavka, on_delete = models.PROTECT)
    narudzba = models.ForeignKey(Narudzba, on_delete = models.PROTECT)

    def __str__(self):
        return f'{self.meniStavka} - {self.narudzba} r.b. {self.redniBroj}'

    @property
    def cijenaSaOpcijama(self):
        from django.db.models import Sum
        from django.db.models import Value
        from django.db.models.functions import Coalesce
        return self.cijenaBezOpcija \
            + self.narudzbastavkaodabraneopcije_set.aggregate(suma=Coalesce(Sum('cijena'), Value(0)))['suma']

class NarudzbaStavkaOdabraneOpcije(models.Model):
    naziv = models.CharField(max_length = 20, help_text = 'Unesite naziv')
    cijena = models.DecimalField(max_digits = 6, decimal_places = 2)
    opcija = models.ForeignKey(Opcija, on_delete = models.PROTECT)
    narudzbaStavka = models.ForeignKey(NarudzbaStavka, on_delete = models.PROTECT) 