from django.db import models
from django.db.models import Sum
from django.utils import timezone


class Building(models.Model):
    name  = models.CharField(verbose_name="Objektname",max_length=200, default=1)
    description = models.TextField(verbose_name="Beschreibung", max_length=1024 * 2)
    photo = models.ImageField(verbose_name="Bild", default=0, blank = True)

    def image_tag(self):
        from django.utils.html import escape
        return u'<img src="%s" />'

    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    class Meta:
        # set the Name of the Table at admin site
        verbose_name_plural = "Gebäude"
        verbose_name = "Gebäude"

    def __str__(self):
        return self.name


class RentalProperty(models.Model):
    name  = models.CharField(verbose_name="Objektname",max_length=200, default=0)
    building  = models.ForeignKey(Building, on_delete=models.CASCADE, default=0)
    description = models.TextField(verbose_name="Beschreibung", max_length=1024 * 2)
    photo = models.ImageField(verbose_name="Bild", default=0, blank = True)

    class Meta:
        # set the Name of the Table at admin site
        verbose_name_plural = "Mietobjekt"
        verbose_name = "Mietobjekt"

    def __str__(self):
        return self.name+' '+self.building.name


class Rent(models.Model):
    description = models.CharField(verbose_name="Beschreibung",max_length=200)
    rent = models.DecimalField(verbose_name="Mietpreis (SFR)",max_digits=6, decimal_places=2)
    start_date = models.DateField(default=timezone.now())
    end_date = models.DateField(default=timezone.now())
    mietobject = models.ForeignKey(RentalProperty, on_delete=models.CASCADE, default=0)
    aktiv = models.BooleanField(default=False)

    class Meta:
        # set the Name of the Table at admin site
        verbose_name_plural = "Mietzins"
        verbose_name = "Mietzins"

    def __str__(self):

        return str(self.mietobject)+' '+str(self.rent)


class Year(models.Model):
    typ = models.IntegerField(default=2010)

    class Meta:
        # set the Name of the Table at admin site
        verbose_name_plural = "Jahr"
        verbose_name = "Jahr"

    def __str__(self):
        return str(self.typ)

class ExtraCosts(models.Model):
    typ = models.CharField(max_length=10, choices=(('Heizung', 'Heizung',),
                                                        ('Wasser', 'Wasser'),
                                                       ('Allg. NK', 'Allg. NK')))
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    a_conto = models.CharField(max_length=10, choices=(('a', 'à conto',),
                                         ('p', 'pauschal')), default='a')
    class Meta:
        # set the Name of the Table at admin site
        verbose_name_plural = "Nebenkosten"
        verbose_name = "Nebenkosten"

    def __str__(self):
        return str(self.typ) +' ' + str(self.amount) + ' ' + str(self.a_conto)


class Renter(models.Model):
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

    class Meta:
        # set the Name of the Table at admin site
        verbose_name_plural = "Mieter"
        verbose_name = "Mieter"

    def __str__(self):
        """
            used for ForeignKey dropDown
        :return:
        """
        return ('{} {} {} ').format(
                                                    self.company,
                                                    self.first_name,
                                                    self.last_name)


class RentProfile(models.Model):
    mieter = models.ForeignKey(Renter, on_delete=models.CASCADE, default =0)
    miete = models.ManyToManyField(Rent)
    nebenkosten = models.ManyToManyField(ExtraCosts)
    start_date = models.DateField(default=timezone.now())
    end_date = models.DateField(default=timezone.now())
    activ = models.BooleanField(verbose_name="aktiv", default=False)

    class Meta:
        # set the Name of the Table at admin site
        verbose_name_plural = "Mietzinsprofil"
        verbose_name = "Mietzinsprofil"

    def __str__(self):
        # total Miete und Nebenkosten
        total = self.miete.aggregate(total_score=Sum('rent'))['total_score'] + \
                self.nebenkosten.aggregate(total_score=Sum('amount'))['total_score']
        return str(self.mieter)+' SFR '+str(total)


class Investment(models.Model):
    project = models.CharField(verbose_name="Projekt", max_length=200)
    mietobject = models.ForeignKey(RentalProperty, on_delete=models.CASCADE, default =0)
    description = models.TextField(verbose_name="Beschreibung", max_length=1024 * 2)
    amount = models.DecimalField(verbose_name="Investition (SFR)", max_digits=10, decimal_places=2)
    datum = models.DateField(default=timezone.now())

    class Meta:
        # set the Name of the Table at admin site
        verbose_name_plural = "Unterhalt"
        verbose_name = "Unterhalt"

    def __str__(self):
        return str(self.mietobject) + ' ' + str(self.project) + ' ' + str(self.amount)


class RentReceipts(models.Model):
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
    mieter = models.ForeignKey(Renter, on_delete=models.CASCADE)
    mietzinsprofil = models.ForeignKey(RentProfile, on_delete=models.CASCADE, default =0)
    amount = models.IntegerField(default=0)
    year  = models.ForeignKey(Year, on_delete=models.CASCADE, default=0)
    description = models.TextField(verbose_name="Bemerkungen", max_length=1024 * 2, blank = True)

    class Meta:
        # set the Name of the Table at admin site
        verbose_name_plural = "Mietzinseingänge"
        verbose_name = "Mietzinseingänge"

    def __str__(self):
        return str(self.mieter) + ' ' + str(self.amount) + ' ' + str(self.datum)

