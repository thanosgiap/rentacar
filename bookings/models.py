from django.db import models
from fleet.models import Car


class Booking(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
    ]

    car = models.ForeignKey(
        Car, on_delete=models.PROTECT, related_name="bookings"
    )

    customer_name = models.CharField(max_length=120)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=30)

    pickup_date = models.DateField()
    dropoff_date = models.DateField()

    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="pending"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.car.name} — {self.customer_name} ({self.pickup_date} → {self.dropoff_date})"