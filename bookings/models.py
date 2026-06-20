from django.db import models
from fleet.models import Car


class Booking(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
    ]
    PAYMENT_METHOD_CHOICES = [
        ("pay_at_pickup", "Pay at pickup"),
        ("card", "Pay by card"),
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
    payment_method = models.CharField(
        max_length=20, choices=PAYMENT_METHOD_CHOICES, default="pay_at_pickup"
    )
    is_paid = models.BooleanField(default=False)
    stripe_session_id = models.CharField(max_length=255, blank=True, default="")
    total_price = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def days(self):
        return max((self.dropoff_date - self.pickup_date).days, 1)

    def save(self, *args, **kwargs):
        self.total_price = self.days * self.car.price_per_day
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.car.name} — {self.customer_name} ({self.pickup_date} → {self.dropoff_date})"
