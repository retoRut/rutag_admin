from django.contrib import admin
# Register your models here.
import json

from django.contrib import admin

from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count, Sum, Min, Max

from .models import Mieter, Mietobjekt, Nebenkosten, Mietzinsprofil, \
    Mietzins, Year, Unterhalt, Mietzinseingaenge, Building


# Register your models here.
@admin.register(Mieter)
class MieterAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Mieter._meta.fields]
    list_filter = ('activ',)

admin.site.register(Year)


@admin.register(Mietobjekt)
class MietobjektAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Mietobjekt._meta.fields]
    list_filter = ('building',)

# ---- Table Nebenkosten
@admin.register(Nebenkosten)
class NebenkostenAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Nebenkosten._meta.fields]


@admin.register(Mietzins)
class MietzinsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Mietzins._meta.fields]


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Building._meta.fields]
   # fields = ('image_tag',)
   # readonly_fields = ('image_tag',)

@admin.register(Unterhalt)
class UnterhaltAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Unterhalt._meta.fields]
    # set the Filter option
    list_filter = ('mietobject',)

    def changelist_view(self, request, extra_context=None):
        """

        :param request:
        :param extra_context:
        :return:
        """
        # Aggregate new subscribers per day
        invest_data_object = (
           Unterhalt.objects.values("mietobject__name","mietobject__building__name").annotate(y=Sum("betrag")).order_by("-mietobject")
        )
        miete_data_object = (
             Mietzins.objects.values("mietobject__name","mietobject__building__name").annotate(y=Sum("rent")).order_by("-mietobject")
        )
        invest_data_building = (
              Unterhalt.objects.values("mietobject__building__name").annotate(y=Sum("betrag"))
        )
        miete_data_building = (
             Mietzins.objects.values("mietobject__building__name").annotate(y=Sum("rent"))
        )
        print('invest_data_object:'+ str(invest_data_object))
        print('miete_data_object:'+ str(miete_data_object))
        print('invest_data_building:'+ str(invest_data_building))
        print('miete_data_building:' + str(miete_data_building))

        # Serialize and attach the chart data to the template context
        as_json_invest_data_object = json.dumps(list(invest_data_object), cls=DjangoJSONEncoder)
        as_json_miete_data_object = json.dumps(list(miete_data_object), cls=DjangoJSONEncoder)
        as_json_invest_data_building = json.dumps(list(invest_data_building), cls=DjangoJSONEncoder)
        as_json_miete_data_building = json.dumps(list(miete_data_building), cls=DjangoJSONEncoder)

        extra_context = extra_context or {"invest_data_object": as_json_invest_data_object,
                                          "miete_data_object": as_json_miete_data_object,
                                          "invest_data_building":as_json_invest_data_building,
                                          "miete_data_building":as_json_miete_data_building }

        return super().changelist_view(request, extra_context=extra_context)

# admin.site.register(Nebenkosten_Typ)
@admin.register(Mietzinsprofil)
class MietzinsprofilAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Mietzinsprofil._meta.fields]

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        """
          show only entries with activ = True
        :param db_field:
        :param request:
        :param kwargs:
        :return:
        """
        if db_field.name == "miete":
            kwargs["queryset"] = Mietzins.objects.filter(aktiv= True)
            print(str(kwargs["queryset"]))
        return super().formfield_for_manytomany(db_field, request, **kwargs)


# ---- Table Mietzinseingaenge
@admin.register(Mietzinseingaenge)
class MietzinseingaengeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Mietzinseingaenge._meta.fields]

    #  list_filter  = ('mieter')
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
          show only entries with activ = True
        :param db_field:
        :param request:
        :param kwargs:
        :return:
        """
        if db_field.name == "mietzinsprofil":
            kwargs["queryset"] = Mietzinsprofil.objects.filter(activ=True)
            # print(" query : " + str(kwargs["queryset"]))
        return super(MietzinseingaengeAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def changelist_view(self, request, extra_context=None):
        # Aggregate new subscribers per day
        chart_data = (
            Mietzinseingaenge.objects.values("year__typ").annotate(y=Sum("betrag")).order_by("-year")
        )
        print('Mieteinnahmen chart:'+ str(chart_data))

        # Serialize and attach the chart data to the template context
        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        extra_context = extra_context or {"chart_data": as_json}

        # Call the superclass changelist_view to render the page
        return super().changelist_view(request, extra_context=extra_context)


