from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "car",
        "customer_name",
        "pickup_date",
        "dropoff_date",
        "status",
    )
    list_filter = ("status", "car")
    search_fields = ("customer_name", "customer_email")