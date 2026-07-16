from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Home, Order

from django.template.loader import render_to_string
from django.http import JsonResponse


def get_filtered_homes(request, base_queryset=None):
    if base_queryset is None:
        homes = Home.objects.filter(active=True).select_related("category")
    else:
        homes = base_queryset

    category = request.GET.get("category")
    bedrooms = request.GET.get("bedrooms")
    bathrooms = request.GET.get("bathrooms")
    stories = request.GET.get("stories")
    sort = request.GET.get("sort")

    if category:
        homes = homes.filter(category__slug=category)

    if bedrooms:
        homes = homes.filter(bedrooms__gte=4) if bedrooms == "4" else homes.filter(bedrooms=bedrooms)

    if bathrooms:
        homes = homes.filter(bathrooms__gte=3) if bathrooms == "3" else homes.filter(bathrooms=bathrooms)

    if stories:
        homes = homes.filter(stories=stories)

    if sort == "newest":
        homes = homes.order_by("-created_at")
    elif sort == "price_low":
        homes = homes.order_by("price")
    elif sort == "price_high":
        homes = homes.order_by("-price")
    elif sort == "largest":
        homes = homes.order_by("-square_feet")
    else:
        homes = homes.order_by("-featured", "name")

    return homes



def home_list(request):
    homes = get_filtered_homes(request)
    categories = Category.objects.filter(active=True)

    return render(request, "shop/shop-page.html", {"homes": homes, "categories": categories})


def ajax_home_filter(request):
    homes = get_filtered_homes(request)

    html = render_to_string("shop/partials/home-list.html", {"homes": homes}, request=request)

    return JsonResponse({
        "html": html,
        "count": homes.count()
    })




def category_list(request):
    categories = Category.objects.filter(active=True)
    return render(request, "shop/category-list.html", {"categories": categories})




def category_detail(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug, active=True)

    # keep filters working inside this category
    request.GET = request.GET.copy()
    request.GET["category"] = category.slug

    homes = get_filtered_homes(
        request,
        Home.objects.filter(category=category, active=True).select_related("category")
    )

    context = {
        "category": category,
        "homes": homes,
        "categories": Category.objects.filter(active=True),
    }

    return render(request, "shop/category-detail.html", context)



def home_detail(request, category_slug, slug):
    home = get_object_or_404(
        Home.objects.select_related("category"),
        active=True,
        category__slug=category_slug,
        slug=slug,
    )

    related_homes = Home.objects.filter(active=True, category=home.category).exclude(pk=home.pk)[:3]

    context = {
        "home": home,
        "gallery": home.gallery.all(),
        "specifications": home.specifications.all(),
        "related_homes": related_homes,
    }
    return render(request, "shop/deailts-page.html", context)



from django.conf import settings
import resend
resend.api_key = settings.RESEND_API_KEY



def checkout(request, slug):
   home = get_object_or_404(Home, slug=slug, active=True)

   if request.method == "POST":
      order = Order.objects.create(
         home=home,
         first_name=request.POST.get("first_name"),
         last_name=request.POST.get("last_name"),
         email=request.POST.get("email"),
         phone=request.POST.get("phone"),
         country=request.POST.get("country"),
         city=request.POST.get("city"),
         address=request.POST.get("address"),
         notes=request.POST.get("notes"),
      )

      home_link = request.build_absolute_uri(home.get_absolute_url())
      html = render_to_string("emails/order_notification.html", {"order": order, "home": home, "home_link": home_link})
      
      print(settings.RESEND_API_KEY)
      try:
         response = resend.Emails.send({
               "from": settings.DEFAULT_FROM_EMAIL,
               "to": [settings.CONTACT_EMAIL],
               "subject": f"New Home Order Request - {home.name}",
               "html": html,
         })
         print(response)
      except Exception as e:
         print("RESEND ERROR:", e)

      return redirect("order_success")

   context = {"home": home}
   return render(request, "shop/checkout.html", context)



def order_success(request):
   return render(request, "shop/order-success.html")
