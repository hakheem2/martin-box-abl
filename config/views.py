from django.http import HttpResponse
def robots_txt(request):
   site = getattr(request, "site_settings", None)
   sitemap_url = f"{site.canonical_domain.rstrip('/')}/sitemap.xml" if site and site.canonical_domain else f"{request.scheme}://{request.get_host()}/sitemap.xml"
   content = f"""
User-agent: *

# Private areas
Disallow: /admin/
Disallow: /cart/
Disallow: /checkout/
Disallow: /accounts/
Disallow: /cms/
Disallow: /documents/

# Internal search pages
Disallow: /search/

# Sitemap
Sitemap: {sitemap_url}
"""

   return HttpResponse(
      content,
   content_type="text/plain; charset=utf-8"
   )
