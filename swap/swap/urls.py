from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import include, path

urlpatterns = [path("admin/", admin.site.urls), path("auth/", include("noauth.urls"))]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
