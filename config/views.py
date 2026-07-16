from django.http import HttpResponse
from django.conf import settings


def robots_txt(request):
   content = f"""
User-agent: *

# Private areas
Disallow: /admin/
Disallow: /cart/
Disallow: /checkout/
Disallow: /accounts/
Disallow: /login/
Disallow: /register/

# Internal search pages
Disallow: /search/

# Sitemap
Sitemap: {request.scheme}://{request.get_host()}/sitemap.xml
"""

   return HttpResponse(
      content,
      content_type="text/plain"
   )