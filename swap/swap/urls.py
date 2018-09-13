from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    url(r"^accounts/", include("django_registration.backends.activation.urls")),
    url(r"^accounts/", include("django.contrib.auth.urls")),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
