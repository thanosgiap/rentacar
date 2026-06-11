from django.contrib import admin
from .models import Car


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "transmission",
        "seats",
        "price_per_day",
        "is_available",
    )
    list_filter = ("category", "transmission", "is_available")
    search_fields = ("name",)