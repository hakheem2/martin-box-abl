from django.db import models


class SiteSettings(models.Model):
   name = models.CharField(max_length=100, default="Martin Boxabl")

   ceo = models.CharField(max_length=100, default="Martin Noe Costas")

   number = models.CharField(max_length=50, blank=True, null=True)

   wa_number = models.CharField(max_length=50, blank=True, null=True)

   email = models.EmailField(blank=True, null=True)
   description = models.TextField(blank=True)
   meta_title = models.CharField(max_length=200, blank=True)
   meta_description = models.CharField(max_length=320, blank=True)
   logo = models.ImageField(upload_to="site/", blank=True, null=True)
   og_image = models.ImageField(upload_to="site/", blank=True, null=True)
   canonical_domain = models.URLField(blank=True, default="https://martinboxabl.com")
   google_analytics_id = models.CharField(max_length=80, blank=True)
   google_tag_manager_id = models.CharField(max_length=80, blank=True)

   address = models.TextField(blank=True, null=True)

   facebook_link = models.URLField(blank=True)
   instagram_link = models.URLField(blank=True)
   tiktok_link = models.URLField(blank=True)

   updated_at = models.DateTimeField(auto_now=True)

   class Meta:
      verbose_name = "Site Settings"
      verbose_name_plural = "Site Settings"

   def __str__(self):
      return self.name
