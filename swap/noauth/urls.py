from django.conf.urls import url

from .views import CodeView, LoginView

urlpatterns = [
    url(r"^code/$", CodeView.as_view(), name="code"),
    url(r"^login/$", LoginView.as_view(), name="login"),
]
