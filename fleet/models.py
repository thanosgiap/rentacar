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

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    seats = models.PositiveSmallIntegerField(default=5)
    transmission = models.CharField(
        max_length=10, choices=TRANSMISSION_CHOICES, default="manual"
    )
    price_per_day = models.DecimalField(max_digits=6, decimal_places=2)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name