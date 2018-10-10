from django.contrib import admin

from .models import Item, ItemImage


class ItemImageAdmin(admin.ModelAdmin):
    readonly_fields = ("full_size_height", "full_size_width", "thumbnail_sizes")


admin.site.register(Item, admin.ModelAdmin)
admin.site.register(ItemImage, ItemImageAdmin)
