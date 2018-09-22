from django.test import TestCase


class FirstTest(TestCase):
    def test_failure(self):
        assert 1 == 2
