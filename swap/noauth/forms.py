from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext as _

from districts.models import District


class LoginForm(forms.Form):
    email = forms.EmailField(label="Work email", max_length=100)

    def clean_email(self):
        email = self.cleaned_data["email"]
        domain = email.split("@")[1]
        try:
            self.district = District.objects.get(email_domain=domain)
        except ObjectDoesNotExist:
            raise forms.ValidationError(
                _("Your email domain is not authorized to sign into this site.")
            )

        return email


class CodeForm(forms.Form):
    email = forms.EmailField(label="Work email", max_length=100)
    code = forms.CharField(label="Code", max_length=20)
