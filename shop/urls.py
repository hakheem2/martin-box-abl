from django.urls import path
from . import views


urlpatterns = [
   path("", views.home_list, name="shop"),

   path("homes/filter/", views.ajax_home_filter, name="ajax_home_filter"),
   path("order-success/", views.order_success, name="order_success"),
   path("home-types/", views.home_types_listing, name="home_types_listing"),
   path("home-categories/", views.category_list, name="category_list"),

   path("<slug:slug>/", views.home_type_detail, name="home_type_detail"),

   path("checkout/<slug:slug>/", views.checkout, name="checkout"),

   path("category/<slug:category_slug>/", views.category_detail, name="category_detail"),
   path("<slug:category_slug>/<slug:slug>/", views.home_detail, name="home_detail"),
   
]