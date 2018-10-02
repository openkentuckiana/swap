import datetime

import mock
from django.http import HttpResponse
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils.translation import gettext as _
from freezegun import freeze_time
from hamcrest import assert_that, equal_to, has_key, none

from districts.models import District
from noauth.models import AuthCode, User

from .forms import CodeForm
from .views import CodeView


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

    @mock.patch("noauth.views.CodeView._validate_and_redirect")
    def test_post_form_with_valid_data_redirects(self, m_validate_and_redirect):
        m_validate_and_redirect.return_value = reverse("noauth:code")
        response = self.client.post(
            reverse("noauth:code"), {"email": "a@example.com", "code": "1"}
        )
        self.assertRedirects(response, reverse("noauth:code"))

    @mock.patch("noauth.views.CodeView._validate_and_redirect")
    def test_post_with_invalid_data_returns_error(self, m_validate_and_redirect):
        m_validate_and_redirect.return_value = None
        response = self.client.post(
            reverse("noauth:code"), {"email": "a@example.com", "code": "1"}
        )
        self.assertFormError(
            response, "form", None, _("Invalid e-mail address or code.")
        )

    @override_settings(NOAUTH_CODE_TTL_MINUTES=5)
    def test_validate_and_redirect_returns_default_path(self):
        email = "test@example.com"
        code = 1234
        d = District.objects.create()
        u = User.objects.create_user(email, email, "NOPE", district=d)

        with freeze_time("09-17-2018 6:30PM") as frozen_datetime:
            ac = AuthCode.objects.create(user=u, code=code)

            frozen_datetime.tick(delta=datetime.timedelta(minutes=4))

            redirect_url = CodeView._validate_and_redirect(email, code)
            assert_that(redirect_url, equal_to("/"))

    @override_settings(NOAUTH_CODE_TTL_MINUTES=5)
    def test_validate_and_redirect_returns_next_page_from_auth_code(self):
        email = "test@example.com"
        code = 1234
        d = District.objects.create()
        u = User.objects.create_user(email, email, "NOPE", district=d)

        with freeze_time("09-17-2018 6:30PM") as frozen_datetime:
            next_page = "/next-page"
            ac = AuthCode.objects.create(user=u, code=code, next_page=next_page)

            frozen_datetime.tick(delta=datetime.timedelta(minutes=4))

            redirect_url = CodeView._validate_and_redirect(email, code)
            assert_that(redirect_url, equal_to(next_page))

    @override_settings(NOAUTH_CODE_TTL_MINUTES=5)
    def test_validate_and_redirect_does_not_find_auth_code_if_ttl_past(self):
        email = "test@example.com"
        code = 1234
        d = District.objects.create()
        u = User.objects.create_user(email, email, "NOPE", district=d)

        with freeze_time("09-17-2018 6:30PM") as frozen_datetime:
            ac = AuthCode.objects.create(user=u, code=code)

            frozen_datetime.tick(delta=datetime.timedelta(minutes=6))

            redirect_url = CodeView._validate_and_redirect(email, code)
            assert_that(redirect_url, none())


class LoginViewTests(TestCase):
    # Write GET tests
    # Write POST tests
    pass
