from django.contrib import admin
from django.utils.html import format_html

from .models import Category, Home, HomeGallery, Specification


# =========================================
# CATEGORY
# =========================================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
   list_display = ("image_preview", "name", "active", "created_at")
   list_filter = ("active",)
   search_fields = ("name",)
   readonly_fields = ("slug", "image_preview")
   ordering = ("name",)

   fieldsets = (
      ("Category", {
         "fields": (
               "name",
               "slug",
               "description",
               "image",
               "image_preview",
               "active",
         )
      }),
   )

   def image_preview(self, obj):
      if obj.image:
         return format_html(
               '<img src="{}" width="70" style="border-radius:8px;">',
               obj.image.url
         )
      return "-"

   image_preview.short_description = "Preview"


# =========================================
# HOME GALLERY INLINE
# =========================================

class HomeGalleryInline(admin.TabularInline):
   model = HomeGallery
   extra = 1
   fields = (
      "image",
      "title",
      "display_order",
   )
   ordering = ("display_order",)


# =========================================
# SPECIFICATIONS INLINE
# =========================================

class SpecificationInline(admin.TabularInline):
   model = Specification
   extra = 2
   fields = (
      "title",
      "value",
      "display_order",
   )
   ordering = ("display_order",)


# =========================================
# HOME
# =========================================

@admin.register(Home)
class HomeAdmin(admin.ModelAdmin):

   inlines = [
      HomeGalleryInline,
      SpecificationInline,
   ]

   list_display = (
      "image_preview",
      "name",
      "category",
      "price",
      "featured",
      "active",
   )

   list_filter = (
      "category",
      "featured",
      "active",
   )

   search_fields = (
      "name",
      "sku",
      "series",
   )

   readonly_fields = (
      "slug",
      "image_preview",
      "created_at",
      "updated_at",
   )

   ordering = (
      "name",
   )

   fieldsets = (

      ("Basic Information", {
         "fields": (
               "category",
               "name",
               "slug",
               "sku",
               "badge",
               "series",
         )
      }),

      ("Pricing", {
         "fields": (
               "price",
               "price_per_sqft",
         )
      }),

      ("Media", {
         "fields": (
               "main_image",
               "image_preview",
               "spec_sheet",
         )
      }),

      ("Descriptions", {
         "fields": (
               "short_description",
               "description",
         )
      }),

      ("Specifications", {
         "fields": (
               "square_feet",
               "bedrooms",
               "bathrooms",
               "stories",
         )
      }),

      ("Status", {
         "fields": (
               "featured",
               "active",
         )
      }),

      ("Dates", {
         "classes": ("collapse",),
         "fields": (
               "created_at",
               "updated_at",
         )
      }),

   )

   def image_preview(self, obj):
      if obj.main_image:
         return format_html(
               '<img src="{}" width="120" style="border-radius:10px;">',
               obj.main_image.url
         )
      return "-"

   image_preview.short_description = "Preview"
