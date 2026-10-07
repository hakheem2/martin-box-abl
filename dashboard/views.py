import logging
from html import escape

from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify
from django.utils.html import strip_tags
from django.utils.http import url_has_allowed_host_and_scheme
from wagtail.images import get_image_model

from blog.models import BlogCategory, BlogIndexPage, BlogPostPage
from core.models import SiteSettings
from shop.models import Home
from .forms import (
    BlogPostForm, DashboardUserCreateForm, ProductForm, ProductGalleryFormSet,
    ProductSpecificationFormSet, SiteSettingsForm,
)

logger = logging.getLogger(__name__)
User = get_user_model()


def dashboard_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect("dashboard:home")
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        if not user.is_staff:
            form.add_error(None, "This account does not have dashboard access.")
        else:
            login(request, user)
            next_url = request.POST.get("next") or request.GET.get("next")
            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
                return redirect(next_url)
            return redirect("dashboard:home")
    return render(request, "dashboard/login.html", {"form": form})


def dashboard_logout(request):
    if request.method == "POST":
        logout(request)
    return redirect("dashboard:login")


def staff_required(view):
    return login_required(user_passes_test(lambda user: user.is_staff)(view), login_url="dashboard:login")


@staff_required
def home(request):
    posts = BlogPostPage.objects.all().order_by("-latest_revision_created_at")[:8]
    products = Home.objects.select_related("category").order_by("-updated_at", "name")[:8]
    context = {
        "active_section": "overview",
        "posts": posts,
        "products": products,
        "post_count": BlogPostPage.objects.count(),
        "published_count": BlogPostPage.objects.live().count(),
        "draft_count": BlogPostPage.objects.not_live().count(),
        "user_count": User.objects.count(),
        "product_count": Home.objects.count(),
    }
    return render(request, "dashboard/home.html", context)


@staff_required
def post_list(request):
    posts = BlogPostPage.objects.all().order_by("-latest_revision_created_at")
    return render(request, "dashboard/posts.html", {"active_section": "posts", "posts": posts})


def _post_parent():
    index = BlogIndexPage.objects.first()
    if index:
        if not index.live:
            index.save_revision().publish()
        return index
    from wagtail.models import Page
    root = Page.get_first_root_node()
    index = BlogIndexPage(title="Blog", slug="blog", intro="Stories, guides, and updates from Martin Boxabl.")
    root.add_child(instance=index)
    index.save_revision().publish()
    return index


def _safe_richtext(text):
    """Store plain text as safe paragraph markup for Wagtail's rich text renderer."""
    paragraphs = [part.strip() for part in text.splitlines() if part.strip()]
    return "".join(f"<p>{escape(strip_tags(part))}</p>" for part in paragraphs)


def _save_post(request, post=None):
    form = BlogPostForm(request.POST or None, request.FILES or None, initial={
        "title": post.title if post else "",
        "slug": post.slug if post else "",
        "excerpt": post.excerpt if post else "",
        "body": strip_tags(post.body.source if hasattr(post.body, "source") else post.body) if post else "",
        "category": post.category_id if post else None,
        "tags": ", ".join(post.tags.names()) if post else "",
        "author": post.author if post else "Martin Boxabl",
    })
    if request.method == "POST" and form.is_valid():
        data = form.cleaned_data
        category = data["category"]
        if data["new_category"].strip():
            category, _ = BlogCategory.objects.get_or_create(
                slug=slugify(data["new_category"]),
                defaults={"name": data["new_category"].strip()},
            )
        slug = data["slug"].strip() or slugify(data["title"])
        if BlogPostPage.objects.exclude(pk=getattr(post, "pk", None)).filter(slug=slug).exists():
            form.add_error("slug", "This URL slug is already used by another post.")
        else:
            with transaction.atomic():
                if post is None:
                    post = BlogPostPage(
                        title=data["title"], slug=slug, excerpt=data["excerpt"],
                        body=_safe_richtext(data["body"]), category=category,
                        author=data["author"],
                    )
                    _post_parent().add_child(instance=post)
                else:
                    post.title = data["title"]
                    post.slug = slug
                    post.excerpt = data["excerpt"]
                    post.body = _safe_richtext(data["body"])
                    post.category = category
                    post.author = data["author"]
                    post.save()
                post.tags.set([tag.strip() for tag in data["tags"].split(",") if tag.strip()])
                if data["featured_image"]:
                    image_model = get_image_model()
                    image = image_model(title=data["featured_image"].name, file=data["featured_image"])
                    image.save()
                    post.featured_image = image
                revision = post.save_revision(user=request.user)
                if data["publish"]:
                    revision.publish()
                messages.success(request, "Post published." if data["publish"] else "Draft saved.")
                return redirect("dashboard:posts")
    return form


@staff_required
def post_create(request):
    form = _save_post(request)
    return render(request, "dashboard/post_form.html", {"active_section": "posts", "form": form, "heading": "Create a post"})


@staff_required
def post_edit(request, post_id):
    post = get_object_or_404(BlogPostPage, pk=post_id)
    form = _save_post(request, post)
    return render(request, "dashboard/post_form.html", {"active_section": "posts", "form": form, "post": post, "heading": "Edit post"})


@staff_required
def product_list(request):
    products = Home.objects.select_related("category", "home_type").annotate(order_count=Count("orders")).order_by("name")
    return render(request, "dashboard/products.html", {"active_section": "products", "products": products})


def _product_editor(request, product=None):
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    gallery_formset = ProductGalleryFormSet(request.POST or None, request.FILES or None, instance=product, prefix="gallery")
    specification_formset = ProductSpecificationFormSet(request.POST or None, instance=product, prefix="specifications")
    if request.method == "POST" and form.is_valid() and gallery_formset.is_valid() and specification_formset.is_valid():
        with transaction.atomic():
            product = form.save()
            gallery_formset.instance = product
            specification_formset.instance = product
            gallery_formset.save()
            specification_formset.save()
        messages.success(request, f"{product.name} saved.")
        return redirect("dashboard:products")
    return form, gallery_formset, specification_formset


@staff_required
def product_create(request):
    form, gallery_formset, specification_formset = _product_editor(request)
    return render(request, "dashboard/product_form.html", {
        "active_section": "products", "form": form,
        "gallery_formset": gallery_formset,
        "specification_formset": specification_formset,
        "heading": "Add a product", "product": None,
    })


@staff_required
def product_edit(request, product_id):
    product = get_object_or_404(Home, pk=product_id)
    form, gallery_formset, specification_formset = _product_editor(request, product)
    return render(request, "dashboard/product_form.html", {
        "active_section": "products", "form": form,
        "gallery_formset": gallery_formset,
        "specification_formset": specification_formset,
        "heading": "Edit product", "product": product,
    })


@staff_required
def product_delete(request, product_id):
    product = get_object_or_404(Home, pk=product_id)
    if request.method == "POST":
        if product.orders.exists():
            messages.error(request, "This product has customer order records. Deactivate it instead to preserve order history.")
            return redirect("dashboard:products")
        name = product.name
        product.delete()
        messages.success(request, f"{name} was deleted.")
        return redirect("dashboard:products")
    return render(request, "dashboard/product_delete.html", {"active_section": "products", "product": product})


@staff_required
def site_settings(request):
    instance = SiteSettings.objects.first()
    form = SiteSettingsForm(request.POST or None, request.FILES or None, instance=instance)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Site information saved.")
        return redirect("dashboard:settings")
    return render(request, "dashboard/settings.html", {"active_section": "settings", "form": form})


@staff_required
def users(request):
    if not request.user.has_perm("auth.view_user") and not request.user.is_superuser:
        raise PermissionDenied
    return render(request, "dashboard/users.html", {"active_section": "users", "users": User.objects.order_by("username")})


@staff_required
def user_create(request):
    if not request.user.has_perm("auth.add_user") and not request.user.is_superuser:
        raise PermissionDenied
    form = DashboardUserCreateForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save(commit=False)
        user.is_staff = form.cleaned_data["is_staff"]
        user.save()
        messages.success(request, f"User {user.username} created.")
        return redirect("dashboard:users")
    return render(request, "dashboard/user_form.html", {"active_section": "users", "form": form})
