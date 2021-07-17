from django.db import models

# Create your models here.
from datetime import datetime, date

from django.contrib import admin
from django.db import models
from django.db.models import Sum
from django.utils import timezone


class Building(models.Model):
    name  = models.CharField(verbose_name="Objektname",max_length=200, default=1)
    description = models.TextField(verbose_name="Beschreibung", max_length=1024 * 2)
    photo = models.ImageField(verbose_name="Bild", default=0, blank = True)

    def image_tag(self):
        from django.utils.html import escape
        return u'<img src="%s" />'# % escape( < URL to the image >)

    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    def __str__(self):
        return self.name


class Mietobjekt(models.Model):
    name  = models.CharField(verbose_name="Objektname",max_length=200, default=0)
    building  = models.ForeignKey(Building, on_delete=models.CASCADE, default=0)
    # mietzins = models.ManyToManyField(Mietzinse)
    #description = models.CharField(verbose_name="Beschreibung",max_length=1000)
    description = models.TextField(verbose_name="Beschreibung", max_length=1024 * 2)
    # rent = models.DecimalField(max_digits=6, decimal_places=2)
    photo = models.ImageField(verbose_name="Bild", default=0, blank = True)

    def __str__(self):
        return self.name+' '+self.building.name


class Mietzins(models.Model):
    #mietobjekt = models.ForeignKey(Mietobjekt, on_delete=models.CASCADE)
    description = models.CharField(verbose_name="Beschreibung",max_length=200)
    rent = models.DecimalField(verbose_name="Mietpreis (SFR)",max_digits=6, decimal_places=2)
    # mieter = models.ForeignKey(Mieter, on_delete=models.CASCADE, default=0)
    start_date = models.DateField(default=timezone.now() )
    end_date = models.DateField(default=timezone.now() )
    mietobject = models.ForeignKey(Mietobjekt, on_delete=models.CASCADE, default=0)
    aktiv = models.BooleanField(default=False)

    def __str__(self):

        return str(self.mietobject)+' '+str(self.rent)


class Year(models.Model):
    typ = models.IntegerField(default=2010)

    def __str__(self):
        return str(self.typ)

class Nebenkosten(models.Model):
    typ =  models.CharField(max_length=10, choices=(('Heizung', 'Heizung',),
                                                        ('Wasser', 'Wasser'),
                                                       ('Allg. NK', 'Allg. NK')))
    betrag = models.DecimalField(max_digits=6, decimal_places=2)
    a_conto =  models.CharField(max_length=10, choices=(('a', 'à conto',),
                                         ('p', 'pauschal')), default='a')

    def __str__(self):
        return str(self.typ)+' '+str(self.betrag)+' '+str(self.a_conto)


class Mieter(models.Model):
    company = models.CharField(verbose_name="Firma", max_length=200,blank = True)
    first_name = models.CharField(verbose_name="Vorname",max_length=200)
    last_name = models.CharField(verbose_name="Nachname", max_length=200)
    email = models.EmailField(verbose_name="Email",blank = True)
    phone_number = models.CharField(verbose_name="Telefonnummer", max_length=200)
    conto_number = models.CharField(verbose_name="IBAN Nummer", max_length=200, default=0)
    address = models.CharField(verbose_name="Strasse", max_length=200, default=0)
    address_Nr = models.IntegerField(verbose_name="Strassennummer", default=0)
    city = models.CharField(verbose_name="Wohnort", max_length=200, default=0)
    city_code = models.IntegerField(verbose_name="PLZ", default=0)
    first_name_2nd = models.CharField(verbose_name="Zweitmieter Vorname", max_length=200,blank = True)
    last_name_2nd = models.CharField(verbose_name="Zweitmieter Nachname", max_length=200, blank = True)
    activ = models.BooleanField(verbose_name="aktiv", default=False)

    def __str__(self):
        """
            used for ForeignKey dropDown
        :return:
        """
        return ('{} {} {} ').format(
                                                    self.company,
                                                    self.first_name,
                                                    self.last_name)


class Mietzinsprofil(models.Model):
    mieter = models.ForeignKey(Mieter, on_delete=models.CASCADE,  default =0)
    miete = models.ManyToManyField(Mietzins)
    nebenkosten = models.ManyToManyField(Nebenkosten)
    start_date = models.DateField(default=timezone.now())
    end_date = models.DateField(default=timezone.now())
    activ = models.BooleanField(verbose_name="aktiv", default=False)

    def __str__(self):
        # total Miete und Nebenkosten
        total = self.miete.aggregate(total_score=Sum('rent'))['total_score'] + \
                self.nebenkosten.aggregate(total_score=Sum('betrag'))['total_score']
        return str(self.mieter)+' SFR '+str(total)


class Unterhalt(models.Model):
    project = models.CharField(verbose_name="Projekt", max_length=200)
    mietobject = models.ForeignKey(Mietobjekt, on_delete=models.CASCADE, default =0)
    description = models.TextField(verbose_name="Beschreibung", max_length=1024 * 2)
    betrag = models.DecimalField(verbose_name="Investition (SFR)",max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.mietobject) + ' ' + str(self.project) + ' ' + str(self.betrag)


class Mietzinseingaenge(models.Model):
    datum = models.DateField(default=timezone.now())
    # ,input_formats=["%Y-%m-%d", ]
    month = models.CharField(max_length=10, choices=(('JA', 'Januar',),
                                                     ('FE', 'Februar'),
                                                     ('MA', 'März'),
                                                     ('AP', 'April'),
                                                     ('MA', 'Mai'),
                                                     ('JN', 'Juni'),
                                                     ('JU', 'Juli'),
                                                     ('AU', 'August'),
                                                     ('SE', 'September'),
                                                     ('OK', 'Oktober'),
                                                     ('NO', 'November'),
                                                     ('DE', 'Dezember'),))
    mieter = models.ForeignKey(Mieter, on_delete=models.CASCADE)
    mietzinsprofil = models.ForeignKey(Mietzinsprofil, on_delete=models.CASCADE, default =0)
    betrag = models.IntegerField(default=0)
    year  = models.ForeignKey(Year, on_delete=models.CASCADE, default=0)

    def __str__(self):
        return str(self.mieter) + ' ' + str(self.betrag) + ' ' + str(self.datum)

