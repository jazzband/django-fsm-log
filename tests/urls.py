try:
    from django.urls import path
    from django.contrib import admin

    urlpatterns = [path('admin', admin.site.urls)]
except ImportError:
    # django < 2.0
    from django.conf.urls import include, url
    from django.contrib import admin

    urlpatterns = [url(r'^admin/', include(admin.site.urls))]
