from django.contrib.gis.db import models as geo_models
from django.db import models
from localflavor.us.models import USStateField, USZipCodeField


class District(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField()
    email_domain = models.CharField(max_length=100, unique=True)
    uri = models.URLField(unique=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"


class Building(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField()
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = USStateField()
    postal_code = USZipCodeField()
    location = geo_models.PointField(blank=True, null=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"
