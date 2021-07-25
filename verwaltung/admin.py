from django.contrib import admin
# Register your models here.
import json

from django.contrib import admin

from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count, Sum, Min, Max

from .models import Renter, RentalProperty, ExtraCosts, RentProfile, \
    Rent, Year, Investment, RentReceipts, Building


# Register your models here.
@admin.register(Renter)
class RenterAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Renter._meta.fields]
    list_filter = ('activ',)

admin.site.register(Year)


@admin.register(RentalProperty)
class RentalPropertyAdmin(admin.ModelAdmin):
    list_display = [field.name for field in RentalProperty._meta.fields]
    list_filter = ('building',)

# ---- Table Nebenkosten
@admin.register(ExtraCosts)
class ExtraCostsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ExtraCosts._meta.fields]


@admin.register(Rent)
class RentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Rent._meta.fields]


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Building._meta.fields]
   # fields = ('image_tag',)
   # readonly_fields = ('image_tag',)

@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Investment._meta.fields]
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
           Investment.objects.values("mietobject__name", "mietobject__building__name").annotate(y=Sum("amount")).order_by("-mietobject")
        )
        miete_data_object = (
             Rent.objects.values("mietobject__name", "mietobject__building__name").annotate(y=Sum("rent")).order_by("-mietobject")
        )
        invest_data_building = (
              Investment.objects.values("mietobject__building__name").annotate(y=Sum("amount"))
        )
        miete_data_building = (
             Rent.objects.values("mietobject__building__name").annotate(y=Sum("rent"))
        )
        print('invest_data_object:'+ str(invest_data_object))
        print('miete_data_object:'+ str(miete_data_object))
      #  print('invest_data_building:'+ str(invest_data_building))
      #  print('miete_data_building:' + str(miete_data_building))

        # Serialize and attach the chart data to the template context
        as_json_invest_data_object = json.dumps(list(invest_data_object), cls=DjangoJSONEncoder)
        as_json_miete_data_object = json.dumps(list(miete_data_object), cls=DjangoJSONEncoder)
        as_json_invest_data_building = json.dumps(list(invest_data_building), cls=DjangoJSONEncoder)
        as_json_miete_data_building = json.dumps(list(miete_data_building), cls=DjangoJSONEncoder)

        print('as_json_invest_data_object:'+ str(as_json_invest_data_object))
        print('miete_data_object:'+ str(as_json_miete_data_object))
       # print('as_json_invest_data_building:'+ str(as_json_invest_data_building))
       # print('miete_data_building:' + str(as_json_miete_data_building))

        extra_context = extra_context or {"invest_data_object": as_json_invest_data_object,
                                          "miete_data_object": as_json_miete_data_object,
                                          "invest_data_building":as_json_invest_data_building,
                                          "miete_data_building":as_json_miete_data_building }

        return super().changelist_view(request, extra_context=extra_context)


@admin.register(RentProfile)
class RentProfileAdmin(admin.ModelAdmin):
    list_display = [field.name for field in RentProfile._meta.fields]

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        """
          show only entries with activ = True
        :param db_field:
        :param request:
        :param kwargs:
        :return:
        """
        if db_field.name == "rent":
            kwargs["queryset"] = Rent.objects.filter(aktiv= True)
            print(str(kwargs["queryset"]))
        return super().formfield_for_manytomany(db_field, request, **kwargs)


# ---- Table RentReceipts
@admin.register(RentReceipts)
class RentReceiptsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in RentReceipts._meta.fields]

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
            kwargs["queryset"] = RentProfile.objects.filter(activ=True)
            # print(" query : " + str(kwargs["queryset"]))
        return super(RentReceiptsAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def changelist_view(self, request, extra_context=None):
        # Aggregate new subscribers per day
        chart_data = (
            RentReceipts.objects.values("year__typ").annotate(y=Sum("amount")).order_by("-year")
        )
        print('Mieteinnahmen chart:'+ str(chart_data))

        # Serialize and attach the chart data to the template context
        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        extra_context = extra_context or {"chart_data": as_json}

        # Call the superclass changelist_view to render the page
        return super().changelist_view(request, extra_context=extra_context)


