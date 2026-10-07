from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("login/", views.dashboard_login, name="login"),
    path("logout/", views.dashboard_logout, name="logout"),
    path("", views.home, name="home"),
    path("posts/", views.post_list, name="posts"),
    path("posts/new/", views.post_create, name="post_create"),
    path("posts/<int:post_id>/edit/", views.post_edit, name="post_edit"),
    path("products/", views.product_list, name="products"),
    path("products/new/", views.product_create, name="product_create"),
    path("products/<int:product_id>/edit/", views.product_edit, name="product_edit"),
    path("products/<int:product_id>/delete/", views.product_delete, name="product_delete"),
    path("settings/", views.site_settings, name="settings"),
    path("users/", views.users, name="users"),
    path("users/new/", views.user_create, name="user_create"),
]
