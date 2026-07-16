from django.shortcuts import render
from shop.models import Category, Home
# Create your views here.
def home(request):
    homes = Home.objects.filter(active=True, featured=True).select_related("category").order_by("?")[:8]

    categories = Category.objects.filter(active=True)
    context = {
        "homes": homes,
        "categories": categories,
    }
    return render(request, "pages/home.html",  context)

def contact(request):
    return render(request, "pages/contact.html")

def about(request):
    return render(request, "pages/about.html")

def gallery(request):
    return render(request, "pages/gallery.html")