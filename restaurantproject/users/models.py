from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

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
    jeUNedostaku = models.BooleanField()

    def __str__(self):
        return self.naziv

class MeniStavka(models.Model):
    redniBroj = models.IntegerField()
    naziv = naziv = models.CharField(max_length = 30, help_text = 'Unesite naziv stavke')
    opis = models.TextField()
    cijena = models.DecimalField(max_digits = 4, decimal_places = 2)
    fotografija = models.ImageField(upload_to = 'photos/menu/%Y/%m/%d')
    nijeUPonudi = models.BooleanField()
    meniStavkaKategorija = models.ForeignKey('MeniStavkaKategorija', on_delete = models.PROTECT)

    def __str__(self):
        return self.naziv

class MeniStavkaTag(models.Model):
    tag = models.CharField(max_length = 20, help_text = 'Unesite tag')

class SastojakMeniStavka(models.Model):
   naziv = models.CharField(max_length = 20, help_text = 'Unesite naziv')
   kolicina = models.IntegerField()
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

class Opcija(models.Model):
    redniBroj = models.IntegerField()
    naziv = models.CharField(max_length = 20, help_text = 'Unesite naziv opcije')
    cijena = models.DecimalField(max_digits = 6, decimal_places = 2)
    imeDodatneSastojke = models.BooleanField()
    grupaOpcija = models.ForeignKey(GrupaOpcija, on_delete = models.CASCADE)

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
    tag = models.CharField(max_length = 20, help_text = 'Unesite tag')
    meniStavkaKategorijaTag = models.ForeignKey(MeniStavkaKategorija, on_delete = models.PROTECT)

class Narudzba(models.Model):
    vrijemeKreiranja = models.DateTimeField(default = timezone.now)
    vrijemeProcesiranja = models.DateTimeField()
    jePrihvacena = models.BooleanField()
    napomena = models.TextField()
    razlogOdbijanja = models.TextField()
    dojam = models.TextField()
    stol = models.IntegerField()
    # TODO: DORADITI NE MOZE SE POKRENUTI ZA SADA !!!
    konobarProcesira = models.ForeignKey(Konobar, on_delete = models.PROTECT, related_name = 'konobar_procesirao', null = True)
    konobarKreira = models.ForeignKey(Konobar, on_delete = models.PROTECT, related_name = 'konobar_kreirao', null = True)

class NarudzbaStavka(models.Model):
    redniBroj = models.IntegerField()
    cijenaBezOpcija = models.DecimalField(max_digits = 6, decimal_places = 2)
    kolicina = models.IntegerField()
    napomena = models.TextField()
    meniStavka = models.ForeignKey(MeniStavka, on_delete = models.PROTECT)
    narudzba = models.ForeignKey(Narudzba, on_delete = models.PROTECT)

class NarudzbaStavkaOdabraneOpcije(models.Model):
    naziv = models.CharField(max_length = 20, help_text = 'Unesite naziv')
    cijena = models.DecimalField(max_digits = 6, decimal_places = 2)
    opcija = models.ForeignKey(Opcija, on_delete = models.PROTECT)
    narudzbaStavka = models.ForeignKey(NarudzbaStavka, on_delete = models.PROTECT) 