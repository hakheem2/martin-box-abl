from django.db import models


class SiteSettings(models.Model):
   name = models.CharField(max_length=100, default="Martin Boxabl")

   number = models.CharField(max_length=50)

   email = models.EmailField()

   address = models.TextField(blank=True)

   facebook_link = models.URLField(blank=True)
   instagram_link = models.URLField(blank=True)
   tiktok_link = models.URLField(blank=True)

   updated_at = models.DateTimeField(auto_now=True)

   class Meta:
      verbose_name = "Site Settings"
      verbose_name_plural = "Site Settings"

   def __str__(self):
      return self.name