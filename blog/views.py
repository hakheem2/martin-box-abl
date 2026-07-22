from django.shortcuts import render
from .models import BlogPostPage


def blog_post(request, slug):
   post = BlogPostPage.objects.live().public().get(slug=slug)

   related_posts = BlogPostPage.objects.live().public().filter(
      category=post.category
   ).exclude(id=post.id)[:3]

   return render(request, "blog/blog_post_page.html", {
      "post": post,
      "related_posts": related_posts,
   })