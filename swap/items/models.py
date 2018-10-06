import string
from random import choices

from django.db import models
from django.utils.text import slugify


class ItemImage(models.Model):
    image = models.ImageField(height_field="height", width_field="width")
    item = models.ForeignKey("Item", blank=True, null=True, on_delete=models.SET_NULL)
    height = models.PositiveIntegerField()
    width = models.PositiveIntegerField()
    deleted = models.BooleanField(default=False)


class Item(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    location = models.ForeignKey("districts.models.Building", on_delete=models.CASCADE)
    owner = models.ForeignKey("noauth.models.User", on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.slug = f"{slugify(self.name)[:45]}-{''.join(choices(string.ascii_lowercase + string.digits, k=10))}"
        super().save(*args, **kwargs)
