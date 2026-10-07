from .models import SiteSettings


def site_settings(request):
   return {
      "site": SiteSettings.objects.first()
   }


from shop.models import Category
def global_categories(request):

   categories = Category.objects.filter(active=True).order_by("name")
   return {
      "footer_categories": categories[:4]
   }


from blog.models import BlogIndexPage
def global_pages(request):
   blog_page = BlogIndexPage.objects.live().public().first()
   return {
      "blog_page": blog_page,
      "blog_url": blog_page.url if blog_page else "/blog/",
   }
