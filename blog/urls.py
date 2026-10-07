from django.urls import path
from wagtail.models import Page
from django.shortcuts import get_object_or_404, render
from .models import BlogIndexPage, BlogPostPage
from django.views.decorators.http import require_GET

@require_GET
def blog_index(request):
   page = BlogIndexPage.objects.live().public().first()
   if page:
      return page.serve(request)
   posts = BlogPostPage.objects.live().public().order_by("-first_published_at")
   return render(request, "blog/blog_index_page.html", {"page": None, "posts": posts})

def blog_post(request, slug):
   post = get_object_or_404(BlogPostPage.objects.live().public(), slug=slug)
   return post.serve(request)

urlpatterns = [
   path("", blog_index, name="blog_index"),
   path("<slug:slug>/", blog_post, name="blog_post"),
]
