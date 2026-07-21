from django.shortcuts import render, redirect
from shop.models import HomeType, Category, Home
import resend

from django.http import JsonResponse
from django.conf import settings
from django.contrib import messages
from django.template.loader import render_to_string


# Create your views here.
def home(request):
    homes = Home.objects.filter(active=True, featured=True).select_related("category").order_by("?")[:6]
    categories = Category.objects.filter(active=True)
    home_types = HomeType.objects.filter(active=True).order_by("?")[:3]
    context = {
        "homes": homes,
        "categories": categories,
        "home_types": home_types,
    }
    return render(request, "pages/home.html",  context)


def contact(request):
    return render(request, "pages/contact.html")


def send_contact(request):
    if request.method == "POST":
        context = {
            "name": request.POST.get("name"),
            "email": request.POST.get("email"),
            "phone": request.POST.get("phone"),
            "subject": request.POST.get("subject"),
            "message": request.POST.get("message"),
        }

        email_html = render_to_string("emails/contact_email.html", context)
        resend.api_key = settings.RESEND_API_KEY

        resend.Emails.send({
            "from": settings.DEFAULT_FROM_EMAIL,
            "to": [settings.CONTACT_EMAIL],
            "subject": context["subject"] or "New Contact Message",
            "html": email_html,
        })

        return JsonResponse({"success": True})

    return JsonResponse({"success": False})


def about(request):
    return render(request, "pages/about.html")


def gallery(request):
    return render(request, "pages/gallery.html")


def custom_404(request, exception):
    return render(request, "404.html", status=404)