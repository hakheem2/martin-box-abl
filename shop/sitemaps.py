from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Home, Category

class StaticViewSitemap(Sitemap):
   priority = 1.0
   changefreq = "daily"

   def items(self):
      return [
         "home",
         "about",
         "contact",
         "shop",
      ]

   def location(self, item):
      return reverse(item)


class CategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Category.objects.filter(active=True)

    def lastmod(self, obj):
        return obj.updated_at if hasattr(obj, "updated_at") else None

   
class HomeSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Home.objects.filter(active=True)

    def lastmod(self, obj):
        return obj.updated_at if hasattr(obj, "updated_at") else None