from django.urls import path
from . import views

app_name = "bookings"

urlpatterns = [
    path("", views.book, name="book"),
    path("pay/<int:booking_id>/", views.pay, name="pay"),
    path("payment-success/", views.payment_success, name="payment_success"),
    path("payment-cancelled/<int:booking_id>/", views.payment_cancelled, name="payment_cancelled"),
    path("success/<int:booking_id>/", views.success, name="success"),
]