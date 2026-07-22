from django.db import models


class SiteSettings(models.Model):
   name = models.CharField(max_length=100, default="Martin Boxabl")

   ceo = models.CharField(max_length=100, default="Martin Noe Costas")

   number = models.CharField(max_length=50, blank=True, null=True)

   wa_number = models.CharField(max_length=50, blank=True, null=True)

   email = models.EmailField(blank=True, null=True)

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