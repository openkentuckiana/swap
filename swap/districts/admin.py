from django.contrib import admin

from .models import Building, District


class DistrictAdmin(admin.ModelAdmin):
    pass


class BuildingAdmin(admin.ModelAdmin):
    pass


admin.site.register(District, DistrictAdmin)
admin.site.register(Building, BuildingAdmin)
