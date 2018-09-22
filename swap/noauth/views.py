import datetime

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ValidationError
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic.edit import FormView

from noauth.models import AuthCode

from .forms import CodeForm, LoginForm
from .models import User


class CodeView(View):
    form_class = CodeForm
    template_name = "code.html"
    success_url = "/"

    def get(self, request, *args, **kwargs):
        email = self.request.GET.get("email")
        code = self.request.GET.get("code")

        if email and code:
            try:
                return self._validate_and_redirect(email, code)
            except:
                pass

        form = self.form_class(initial={"email": email})
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            code = form.cleaned_data["code"]
            try:
                return self._validate_and_redirect(email, code)
            except:
                form.add_error(
                    None,
                    ValidationError(
                        _("Invalid e-mail address or code."),
                        code="invalid_email_or_code",
                    ),
                )

        return render(request, self.template_name, {"form": form})

    def _validate_and_redirect(self, email, code):
        valid_timestamp_start = timezone.now() - datetime.timedelta(
            minutes=getattr(settings, "NOAUTH_CODE_TTL_MINUTES", 5)
        )
        auth_code = AuthCode.objects.get(
            user__username=email, code=code, timestamp__gte=valid_timestamp_start
        )
        next_page = auth_code.next_page
        auth_code.delete()
        return redirect(next_page or "/")


class LoginView(FormView):
    template_name = "login.html"
    form_class = LoginForm
    success_url = reverse_lazy("code")

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        district = form.district
        user = self.get_user(email)
        if not user:
            user = self.create_user(email, district)

        AuthCode.create_code_for_user(user)

        self.success_url += f"?email={user.username}"

        return super().form_valid(form)

    def create_user(self, email, district):
        return User.objects.create_user(email, email, "NOPE", district=district)

    def get_user(self, email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
