from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext as _
from hamcrest import assert_that, has_key

from districts.models import District

from .forms import CodeForm, LoginForm


class LoginFormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase (don't modify this object)
        cls.district1 = District.objects.create(
            name="Test district1",
            email_domain="example1.com",
            uri="https://example1.com",
        )
        cls.district2 = District.objects.create(
            name="Test district2",
            email_domain="example2.com",
            uri="https://example2.com",
        )

    def test_verify_email_required(self):
        form = CodeForm(data={})
        self.assertFalse(form.is_valid())
        assert_that(form.errors, has_key("email"))

    def test_district1_email_accepted_as_valid(self):
        data = {"email": "jane@example1.com"}
        form = LoginForm(data)
        self.assertTrue(form.is_valid())

    def test_district2_email_accepted_as_valid(self):
        data = {"email": "jane@example2.com"}
        form = LoginForm(data)
        self.assertTrue(form.is_valid())

    def test_unknown_email_domain_rejected_as_invalid(self):
        data = {"email": "jane@unknown.com"}
        form = LoginForm(data)
        self.assertFalse(form.is_valid())

    def test_unknown_email_domain_error_message(self):
        data = {"email": "jane@unknown.com"}
        form = LoginForm(data)
        response = self.client.post(reverse("noauth:login"), data)
        self.assertFormError(
            response,
            "form",
            "email",
            _("Your email domain is not authorized to sign into this site."),
        )

    def test_deactivated_district_email_domain_rejected_as_invalid(self):
        District.objects.create(
            name="Test district3",
            email_domain="example3.com",
            uri="https://example3.com",
            deleted=True,
        )
        data = {"email": "jane@example3.com"}
        form = LoginForm(data)
        self.assertFalse(form.is_valid())

    def test_deactivated_district_email_domain_error_message(self):
        District.objects.create(
            name="Test district3",
            email_domain="example3.com",
            uri="https://example3.com",
            deleted=True,
        )
        data = {"email": "jane@example3.com"}
        response = self.client.post(reverse("noauth:login"), data)
        self.assertFormError(
            response,
            "form",
            "email",
            _("Your email domain is not authorized to sign into this site."),
        )


class CodeFormTests(TestCase):
    def test_verify_email_and_code_are_accepted(self):
        data = {"email": "joe@domain.com", "code": 123}
        form = CodeForm(data)
        self.assertTrue(form.is_valid())

    def test_verify_email_required(self):
        data = {"code": 123}
        form = CodeForm(data)
        self.assertFalse(form.is_valid())
        assert_that(form.errors, has_key("email"))

    def test_verify_code_required(self):
        data = {"email": "joe@domain.com"}
        form = CodeForm(data)
        self.assertFalse(form.is_valid())
        assert_that(form.errors, has_key("code"))
