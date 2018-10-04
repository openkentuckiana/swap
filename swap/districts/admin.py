from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin

from .models import Building, District


class BuildingAdmin(OSMGeoAdmin):
    modifiable = False


admin.site.register(District, admin.ModelAdmin)
admin.site.register(Building, BuildingAdmin)
