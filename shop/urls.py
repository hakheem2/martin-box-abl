from django.urls import path
from . import views


urlpatterns = [
   path("", views.home_list, name="shop"),
   path("homes/filter/", views.ajax_home_filter, name="ajax_home_filter"),
   path("checkout/<slug:slug>/", views.checkout, name="checkout"),
   path("<slug:category_slug>/<slug:slug>/", views.home_detail, name="home_detail"),
   path("order-success/", views.order_success, name="order_success"),
]