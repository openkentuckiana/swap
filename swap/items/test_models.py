from django.test import TestCase
from hamcrest import assert_that, starts_with

from districts.models import Building, District
from noauth.models import User

from .models import Item


class ItemModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.d = District.objects.create()
        cls.b = Building.objects.create(district=cls.d)
        cls.u = User.objects.create(
            is_active=True, district=cls.d, email="eleanor@shellstrop.com"
        )

    def test_slug_generated(self):
        forty_five_character_name = "a" * 45
        i = Item.objects.create(
            name=forty_five_character_name,
            location=ItemModelTests.b,
            owner=ItemModelTests.u,
        )
        assert_that(i.slug, starts_with(f"{forty_five_character_name}-"))

    def test_truncated_slug_generated(self):
        sixty_character_name = "a" * 60
        i = Item.objects.create(
            name=sixty_character_name, location=ItemModelTests.b, owner=ItemModelTests.u
        )
        assert_that(i.slug, starts_with(f"{sixty_character_name[:45]}-"))


class ItemImageModelTests(TestCase):
    pass
