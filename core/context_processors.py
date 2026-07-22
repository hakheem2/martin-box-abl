from .models import SiteSettings


def site_settings(request):
   return {
      "site": SiteSettings.objects.first()
   }


from shop.models import Category
import random
def global_categories(request):

   categories = list(Category.objects.filter(active=True))
   random.shuffle(categories)

   return {
      "footer_categories": categories[:4]
   }


from blog.models import BlogIndexPage
def global_pages(request):
   return {
      "blog_page": BlogIndexPage.objects.live().public().first()
   }