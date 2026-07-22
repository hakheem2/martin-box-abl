from django.db import models
from django.utils.text import slugify
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.images.models import Image
from wagtail.admin.panels import FieldPanel
from taggit.managers import TaggableManager


class BlogCategory(models.Model):
   name = models.CharField(max_length=100, unique=True)
   slug = models.SlugField(unique=True, blank=True)
   description = models.TextField(blank=True)

   class Meta:
      verbose_name = "Blog Category"
      verbose_name_plural = "Blog Categories"

   def save(self, *args, **kwargs):
      if not self.slug:
         self.slug = slugify(self.name)
      super().save(*args, **kwargs)

   def __str__(self):
      return self.name


class BlogIndexPage(Page):
   intro = models.TextField(
      blank=True, help_text="Short introduction displayed above blog posts."
   )

   subpage_types = ["blog.BlogPostPage"]

   content_panels = Page.content_panels + [
      FieldPanel("intro"),
   ]

   def get_context(self, request):
      context = super().get_context(request)
      posts = self.get_children().live().specific().order_by("-first_published_at")
      context["posts"] = posts
      context["categories"] = BlogCategory.objects.all()
      return context


class BlogPostPage(Page):
   featured_image = models.ForeignKey(
      Image, null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
   )
   excerpt = models.TextField(blank=True, max_length=300)
   body = RichTextField()
   category = models.ForeignKey(
      BlogCategory, null=True, blank=True, on_delete=models.SET_NULL, related_name="posts"
   )
   tags = TaggableManager(blank=True)
   author = models.CharField(max_length=100, default="Martin Boxabl")

   content_panels = Page.content_panels + [
      FieldPanel("featured_image"),
      FieldPanel("excerpt"),
      FieldPanel("body"),
      FieldPanel("category"),
      FieldPanel("tags"),
      FieldPanel("author"),
   ]

   parent_page_types = ["blog.BlogIndexPage"]

   def get_context(self, request):
      context = super().get_context(request)
      related_posts = (
         BlogPostPage.objects.live()
         .public()
         .filter(category=self.category)
         .exclude(id=self.id)
         .order_by("-first_published_at")[:3]
      )
      context["related_posts"] = related_posts
      return context