try:
    from django.contrib import admin
    from django.urls import path

    urlpatterns = [path("admin", admin.site.urls)]
except ImportError:
    # django < 2.0
    from django.contrib import admin
    from django.urls import include, path

    urlpatterns = [path("admin/", include(admin.site.urls))]
