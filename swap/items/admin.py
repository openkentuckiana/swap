from django.contrib import admin

from .models import Item, ItemImage

admin.site.register(Item, admin.ModelAdmin)
admin.site.register(ItemImage, admin.ModelAdmin)
