"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# WIGTAIL CONFIG
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls

# SITEMAPS CONFIG
from .views import robots_txt
from django.contrib.sitemaps.views import sitemap
from shop.sitemaps import StaticViewSitemap, CategorySitemap, HomeSitemap, BlogSitemap

sitemaps = {
    "static": StaticViewSitemap,
    "categories": CategorySitemap,
    "homes": HomeSitemap,
    "blog": BlogSitemap,
}


urlpatterns = [
    path("dashboard/", include("dashboard.urls")),
    path("admin/", admin.site.urls),

    path("", include("core.urls")),
    path("homes-for-sale/", include("shop.urls")),
    path("blog/", include("blog.urls")),

    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
    path("robots.txt", robots_txt, name="robots_txt"),

    # Wagtail
    path("cms/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("", include(wagtail_urls)),
]


handler404 = "core.views.custom_404"
handler400 = "core.views.custom_400"
handler403 = "core.views.custom_403"
handler500 = "core.views.custom_500"

if settings.DEBUG and not getattr(settings, "CLOUDINARY_URL", ""):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
