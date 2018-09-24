import string
from secrets import choice

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from districts.models import District

DEFAULT_CODE_LENGTH = 6


class User(AbstractUser):
    district = models.ForeignKey(District, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.username}"


class AuthCode(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="auth_codes",
        editable=False,
        on_delete=models.CASCADE,
    )
    code = models.CharField(max_length=20, editable=False)
    timestamp = models.DateTimeField(editable=False, auto_now=True)
    next_page = models.TextField(editable=False, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.code}"

    @classmethod
    def create_code_for_user(cls, user, next_page=None):
        if not user.is_active:
            return None

        code = cls.generate_code()
        AuthCode.objects.filter(user=user).delete()
        return AuthCode.objects.create(user=user, code=code, next_page=next_page)

    @classmethod
    def generate_code(cls):
        code_length = getattr(settings, "NOAUTH_CODE_LENGTH", DEFAULT_CODE_LENGTH)
        return "".join(choice(string.digits) for i in range(code_length))
