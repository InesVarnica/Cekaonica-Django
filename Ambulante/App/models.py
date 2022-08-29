from asyncio.windows_events import NULL
from doctest import BLANKLINE_MARKER
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime







# Create your models here.

class Korisnik(AbstractUser):
    ROLES = (('dr', 'liječnik'), ('spec', 'specijalist'),('admin', 'administrator'),('ms', 'medicinska sestra'),('vms', 'viša medicinska sestra'))
    role = models.CharField(max_length=50, choices=ROLES)


    def __str__(self):
        return '%s %s %s ' % (self.username, self.email , self.role )


class Radilišta(models.Model):

    KLINIKA = (('KIR','Kirurgija'),('PED','Pedijatrija'),('INT','Unutarnje bolesti'),('ORT','Otorinolaringologija'),('NRL','Neurologija'),('GIN','Ginekologija'),('PSI','Psihijatrija'),('KOZ','Kožne bolesti'))
    klinika = models.CharField(max_length=50, choices=KLINIKA)
    naziv = models.CharField(max_length=50)

    def __str__(self):
        return '%s %s ' % (self.klinika, self.naziv )


class Radilište_korisnik(models.Model):
    zaposlenik = models.ForeignKey(Korisnik,  on_delete=models.CASCADE, related_name = 'radilište_korisnik')
    radilište = models.ForeignKey(Radilišta,  on_delete=models.CASCADE, related_name = 'radilište_korisnik')

    def __str__(self):
        return '%s %s ' % (self.zaposlenik, self.radilište )




    def __str__(self):
        return '%s %s %s %s %s %s %s' % (self.naziv_nalaza, self.razlog_dolaska, self.anamneza, self.terapija, self.zaključak, self.naziv_radilišta, self.zaposlenik)

class RegistarPacijenata(models.Model):
    STATUS_OSIGURANJA = (('DA', 'Važeće'), ('NE', 'Nevažeće'))
    MBO = models.IntegerField(blank=True, null=True)
    ime = models.CharField(max_length=50)
    prezime = models.CharField(max_length=50)
    datum_rođenja =  models.CharField(blank=True, null=True, max_length=11)
    email = models.EmailField(max_length=50, blank=True)
    broj_telefona = models.IntegerField(blank=True, null=True)
    adresa = models.CharField(max_length=50, blank=True, null=True)
    status_osiguranja = models.CharField(max_length=50, choices=STATUS_OSIGURANJA, blank=True, )
    datum_police_osiguranja = models.CharField(blank=True, null=True, max_length=11)
    


    def __str__(self):
        return '%s %s %s %s %s %s %s %s' % (self.MBO, self.ime, self.prezime, self.email, self.broj_telefona, self.adresa, self.status_osiguranja, self.datum_police_osiguranja, )

class ŠifrarnikUtrošak(models.Model):
    šifra = models.CharField(max_length=6)
    naziv = models.CharField(max_length=100)
    cijena = models.FloatField()
    

    def __str__(self):
        return '%s %s  ' % (self.šifra, self.naziv, )

class Uputnice(models.Model):
    TIP = (('A1','Konzilijarni pregled'),('A2','Kontrolni konzilijarni pregled'),('C1','Pregled i cjelovita obrada u specijalističkoj zdravstvenoj zaštiti'),('C2','Pregled i obrada kroz Objedinjeni hitni bolnički prijam'),('D1','Ambulantno liječenje'),('D2',' Dnevna bolnica'),('NEMA','Bez_uputnice'))
    tip = models.CharField(max_length=50, choices=TIP)

    def __str__(self):
        return '%s ' % (self.tip)


class Posjeta(models.Model):
    STATUS_OTPUSTA= (('K','Kući'),('H','Hospitalizacija'),('O','Opservacija'),('PP','Prekinut pregled'))
    pacijent = models.ForeignKey(RegistarPacijenata,  on_delete=models.CASCADE, related_name = 'posjeta')
    naziv_radilišta = models.ForeignKey(Radilišta,  on_delete=models.CASCADE, related_name = 'posjeta')
    zaposlenik = models.ForeignKey(Korisnik,  on_delete=models.CASCADE, related_name = 'posjeta')
    datum = models.DateTimeField(auto_now_add=True)
    uputnica = models.ForeignKey(Uputnice, on_delete=models.CASCADE, related_name = 'posjeta')
    status_otpusta = models.CharField(max_length=50, choices=STATUS_OTPUSTA)
    vrijeme_otpusta = models.DateTimeField(null=True, blank = True,auto_now_add=True )




    def __str__(self):
        return '%s %s %s %s %s %s' % (self.naziv_radilišta, self.pacijent, self.zaposlenik, self.datum, self.uputnica, self.vrijeme_otpusta)

class Nalaz(models.Model):
    dijagnoza = models.CharField(max_length=5,blank=True, null = True)
    naziv_nalaza = models.CharField(max_length=50)
    razlog_dolaska = models.TextField(max_length=200,blank=True, null = True)
    anamneza = models.TextField(max_length=200,blank=True, null = True)
    terapija = models.TextField(max_length=200,blank=True, null = True)
    zaključak = models.TextField(max_length=200,blank=True, null = True)
    naziv_radilišta = models.ForeignKey(Radilišta,  on_delete=models.CASCADE, related_name = 'nalaz')
    zaposlenik = models.ForeignKey(Korisnik,  on_delete=models.CASCADE, related_name = 'nalaz', blank=True, null = True)
    zaposlenik2 = models.ForeignKey(Korisnik,  on_delete=models.CASCADE, related_name = 'nalaz2', blank=True,null = True)
    posjeta = models.ForeignKey(Posjeta, on_delete=models.CASCADE, related_name = 'nalazi',blank=True ,null=True)

    def __str__(self):
        return '%s %s %s %s %s %s %s %s %s %s ' % (self.naziv_nalaza, self.razlog_dolaska, self.anamneza, self.terapija, self.zaključak, self.naziv_radilišta, self.zaposlenik, self.zaposlenik2, self.posjeta, self.dijagnoza)

class Utrošak_posjeta(models.Model):
    utrošak = models.ForeignKey(ŠifrarnikUtrošak, on_delete=models.CASCADE, related_name = 'utrošak_posjeta', blank=True,null=True)
    posjeta = models.ForeignKey(Posjeta, on_delete=models.CASCADE, related_name = 'utrošak_posjeta', blank=True,null=True)
    količina_utroška = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return '%s %s %s' % (self.utrošak, self.količina_utroška, self.posjeta)

class Blagajna(models.Model):
    posjeta = models.ForeignKey(Posjeta, on_delete=models.CASCADE, related_name = 'blagajna', blank=True,null=True)
    cijena = models.FloatField()
    zaposlenik = models.ForeignKey(Korisnik,  on_delete=models.CASCADE, related_name = 'blagajna')

    def __str__(self):
        return '%s %s %s' % (self.posjeta, self.cijena, self.zaposlenik)

