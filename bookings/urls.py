from django.urls import path
from . import views

app_name = "bookings"

urlpatterns = [
    path("", views.book, name="book"),
    path("success/<int:booking_id>/", views.success, name="success"),
]