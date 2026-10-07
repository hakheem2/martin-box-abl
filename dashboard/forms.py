from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from blog.models import BlogCategory, BlogPostPage
from core.models import SiteSettings
from shop.models import Home, HomeGallery, Specification
from django.forms import inlineformset_factory


class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        exclude = ("updated_at",)
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
            "meta_description": forms.Textarea(attrs={"rows": 3}),
            "address": forms.Textarea(attrs={"rows": 2}),
        }


class BlogPostForm(forms.Form):
    title = forms.CharField(max_length=255)
    slug = forms.SlugField(max_length=255, required=False)
    excerpt = forms.CharField(max_length=300, widget=forms.Textarea(attrs={"rows": 3}))
    body = forms.CharField(widget=forms.Textarea(attrs={"rows": 14, "placeholder": "Write your article. Separate paragraphs with a blank line."}))
    category = forms.ModelChoiceField(queryset=BlogCategory.objects.all(), required=False)
    new_category = forms.CharField(max_length=100, required=False)
    tags = forms.CharField(required=False, help_text="Separate tags with commas.")
    author = forms.CharField(max_length=100, initial="Martin Boxabl")
    featured_image = forms.ImageField(required=False)
    publish = forms.BooleanField(required=False, label="Publish this post now")


class DashboardUserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)
    is_staff = forms.BooleanField(required=False, label="Can access the dashboard")

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("username", "email", "first_name", "last_name", "is_staff")


class ProductForm(forms.ModelForm):
    class Meta:
        model = Home
        exclude = ("created_at", "updated_at")
        widgets = {
            "short_description": forms.Textarea(attrs={"rows": 3}),
            "description": forms.Textarea(attrs={"rows": 6}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].required = True
        if self.instance and self.instance.pk:
            self.fields["main_image"].required = False


ProductGalleryFormSet = inlineformset_factory(
    Home, HomeGallery, fields=("image", "title", "display_order"), extra=2, can_delete=True,
)
ProductSpecificationFormSet = inlineformset_factory(
    Home, Specification, fields=("title", "value", "display_order"), extra=3, can_delete=True,
)
