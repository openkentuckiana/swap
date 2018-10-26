from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin

from lib.admin import SoftDeleteModelAdmin

from .models import Building, District


class BuildingAdmin(OSMGeoAdmin, SoftDeleteModelAdmin):
    list_display = ("name", "deleted_at")
    modifiable = False


class DistrictAdmin(SoftDeleteModelAdmin):
    list_display = ("name", "deleted_at")


admin.site.register(Building, BuildingAdmin)
admin.site.register(District, DistrictAdmin)
