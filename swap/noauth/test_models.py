from django.test import TestCase, override_settings
from hamcrest import assert_that, equal_to, none

from districts.models import District

from .models import DEFAULT_CODE_LENGTH, AuthCode, User


class AuthCodeModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.d = District.objects.create()

    def setUp(self):
        self.u = User.objects.create(is_active=True, district=AuthCodeModelTests.d)

    def test_create_code_for_user_returns_none_for_inactive_user(self):
        self.u.is_active = False
        self.u.save()
        assert_that(AuthCode.create_code_for_user(self.u), none())

    def test_create_code_for_user_creates_new_code(self):
        expected_auth_code = AuthCode.create_code_for_user(self.u)
        actual_auth_code = AuthCode.objects.get(
            user=self.u, code=expected_auth_code.code
        )
        assert_that(expected_auth_code.code, equal_to(actual_auth_code.code))

    def test_generate_code_creates_code_of_default_length(self):
        code = AuthCode.create_code_for_user(self.u).code
        assert_that(len(code), equal_to(DEFAULT_CODE_LENGTH))

    @override_settings(NOAUTH_CODE_LENGTH=19)
    def test_generate_code_creates_code_of_length_defined_in_settings(self):
        code = AuthCode.create_code_for_user(self.u).code
        assert_that(len(code), equal_to(19))
