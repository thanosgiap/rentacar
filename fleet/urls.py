from django.urls import path
from . import views

app_name = "fleet"

urlpatterns = [
    path("", views.car_list, name="car_list"),
    path("contact/", views.contact, name="contact"),
]