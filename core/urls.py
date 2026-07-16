from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path('contact/', views.contact, name='contact'),
    path('gallery/', views.gallery, name='gallery'),

    path("send-contact/", views.send_contact, name="send_contact"),
]