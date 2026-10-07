import logging

from django.shortcuts import render
from shop.models import HomeType, Category, Home
from django.http import JsonResponse
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.template.loader import render_to_string
import resend

from blog.models import BlogPostPage

logger = logging.getLogger(__name__)


# Create your views here.
def home(request):
    homes = Home.objects.filter(active=True, featured=True).select_related("category").order_by("-updated_at", "name")[:6]
    categories = Category.objects.filter(active=True)
    home_types = HomeType.objects.filter(active=True).order_by("name")[:3]
    blog_posts = BlogPostPage.objects.live().public().order_by("-first_published_at")[:3]
    context = {
        "homes": homes,
        "categories": categories,
        "home_types": home_types,
        "blog_posts": blog_posts,
    }
    return render(request, "pages/home.html",  context)


def contact(request):
    return render(request, "pages/contact.html")


def send_contact(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "POST required."}, status=405)

    context = {
        "name": request.POST.get("name", "").strip(),
        "email": request.POST.get("email", "").strip(),
        "phone": request.POST.get("phone", "").strip(),
        "subject": request.POST.get("subject", "").strip()[:180],
        "message": request.POST.get("message", "").strip(),
    }
    if not all((context["name"], context["email"], context["message"])):
        return JsonResponse({"success": False, "error": "Name, email, and message are required."}, status=400)
    try:
        validate_email(context["email"])
    except ValidationError:
        return JsonResponse({"success": False, "error": "Enter a valid email address."}, status=400)
    if not settings.RESEND_API_KEY or not settings.DEFAULT_FROM_EMAIL or not settings.SUPPORT_EMAIL:
        logger.error("Contact email is not configured.")
        return JsonResponse({"success": False, "error": "Email is temporarily unavailable."}, status=503)

    html = render_to_string("emails/contact_email.html", context)
    try:
        resend.api_key = settings.RESEND_API_KEY
        resend.Emails.send({
            "from": settings.DEFAULT_FROM_EMAIL,
            "to": [settings.SUPPORT_EMAIL],
            "reply_to": [context["email"]],
            "subject": context["subject"] or "New Contact Message",
            "html": html,
            "text": f"Message from {context['name']} ({context['email']}):\n\n{context['message']}",
        })
    except Exception:
        logger.exception("Failed to send contact message")
        return JsonResponse({"success": False, "error": "Message could not be sent. Please try again later."}, status=503)
    return JsonResponse({"success": True})


def about(request):
    return render(request, "pages/about.html")


def gallery(request):
    return render(request, "pages/gallery.html")


def custom_404(request, exception):
    return render(request, "404.html", status=404)


def custom_400(request, exception):
    return render(request, "errors/400.html", status=400)


def custom_403(request, exception):
    return render(request, "errors/403.html", status=403)


def custom_401(request):
    return render(request, "errors/401.html", status=401)


def custom_500(request):
    return render(request, "errors/500.html", status=500)
