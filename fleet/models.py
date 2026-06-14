from django.db import models


class Car(models.Model):
    CATEGORY_CHOICES = [
        ("economy", "Economy"),
        ("compact", "Compact"),
        ("suv", "SUV"),
        ("van", "Van"),
        ("luxury", "Luxury"),
    ]
    TRANSMISSION_CHOICES = [
        ("manual", "Manual"),
        ("automatic", "Automatic"),
    ]
    FUEL_CHOICES = [
        ("petrol", "Petrol"),
        ("diesel", "Diesel"),
        ("hybrid", "Hybrid"),
        ("electric", "Electric"),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    seats = models.PositiveSmallIntegerField(default=5)
    doors = models.PositiveSmallIntegerField(default=5)
    luggage = models.PositiveSmallIntegerField(default=2, help_text="Number of large bags")
    transmission = models.CharField(
        max_length=10, choices=TRANSMISSION_CHOICES, default="manual"
    )
    fuel_type = models.CharField(max_length=10, choices=FUEL_CHOICES, default="petrol")
    mileage_km = models.PositiveIntegerField(default=0, help_text="Total km on the odometer")
    price_per_day = models.DecimalField(max_digits=6, decimal_places=2)
    
    photo = models.ImageField(upload_to="cars/", blank=True, null=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name