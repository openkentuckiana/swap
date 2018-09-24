import mock
from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext as _
from hamcrest import assert_that, equal_to, has_key, none

from districts.models import District

from .forms import CodeForm


class CodeViewTests(TestCase):
    @mock.patch("noauth.views.CodeView._validate_and_redirect")
    def test_get_with_code_and_email_calls_validate_method(
        self, m_validate_and_redirect
    ):
        m_validate_and_redirect.return_value = None

        response = self.client.get(f'{reverse("noauth:code")}?email=a&code=1')

        m_validate_and_redirect.assert_called_once_with("a", "1")

    def test_get_with_code_and_no_email_returns_blank_form(self):
        response = self.client.get(f'{reverse("noauth:code")}?code=1')
        form = response.context["form"]
        assert_that(form.initial, has_key("email"))
        assert_that(form.initial["email"], none())
        self.assertTrue(isinstance(form, CodeForm))

    def test_get_with_email_and_no_code_returns_form_eith_email(self):
        response = self.client.get(f'{reverse("noauth:code")}?email=a')
        form = response.context["form"]
        assert_that(form.initial, has_key("email"))
        assert_that(form.initial["email"], equal_to("a"))
        self.assertTrue(isinstance(form, CodeForm))

    # Write POST tests


class LoginViewTests(TestCase):
    # Write GET tests
    # Write POST tests
    pass
