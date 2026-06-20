from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "car",
        "customer_name",
        "pickup_date",
        "dropoff_date",
        "total_price",
        "status",
        "payment_method",
        "is_paid",
    )
    list_filter = ("status", "payment_method", "is_paid", "car")
    search_fields = ("customer_name", "customer_email")