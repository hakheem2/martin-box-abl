from django.contrib import admin
from .models import SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "number")
    fieldsets = (
        ("Site identity", {"fields": ("name", "ceo", "description", "logo", "og_image", "canonical_domain")}),
        ("Contact details", {"fields": ("number", "wa_number", "email", "address")}),
        ("Search and analytics", {"fields": ("meta_title", "meta_description", "google_analytics_id", "google_tag_manager_id")}),
        ("Social links", {"fields": ("facebook_link", "instagram_link", "tiktok_link")}),
        ("Maintenance", {"fields": ("updated_at",)}),
    )
    readonly_fields = ("updated_at",)

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists() and super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False
