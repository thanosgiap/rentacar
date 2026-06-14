from fleet.models import Car
from .models import Booking
from django.conf import settings
from django.core.mail import send_mail

# A booking in one of these statuses is actively holding the car.
BLOCKING_STATUSES = ["pending", "confirmed"]


def is_car_available(car, pickup_date, dropoff_date, exclude_booking_id=None):
    """True if `car` has no conflicting booking over the given date range."""
    conflicts = car.bookings.filter(
        status__in=BLOCKING_STATUSES,
        pickup_date__lte=dropoff_date,
        dropoff_date__gte=pickup_date,
    )
    if exclude_booking_id is not None:
        conflicts = conflicts.exclude(id=exclude_booking_id)
    return not conflicts.exists()


def available_cars(pickup_date, dropoff_date):
    """Every bookable car that is free over the given date range."""
    taken_ids = Booking.objects.filter(
        status__in=BLOCKING_STATUSES,
        pickup_date__lte=dropoff_date,
        dropoff_date__gte=pickup_date,
    ).values_list("car_id", flat=True)
    return Car.objects.filter(is_available=True).exclude(id__in=taken_ids)

def send_booking_emails(booking):
    # Confirmation to the customer
    send_mail(
        subject="Your RentACar booking is confirmed",
        message=(
            f"Hi {booking.customer_name},\n\n"
            f"Your booking is confirmed:\n"
            f"  Car: {booking.car.name}\n"
            f"  From: {booking.pickup_date}\n"
            f"  To:   {booking.dropoff_date}\n"
            f"  Total: €{booking.total_price}\n\n"
            f"See you soon!\nRentACar"
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[booking.customer_email],
        fail_silently=False,
    )

    # Alert to the owner
    send_mail(
        subject=f"New booking — {booking.car.name}",
        message=(
            f"New booking received:\n\n"
            f"  Car:      {booking.car.name}\n"
            f"  Customer: {booking.customer_name}\n"
            f"  Email:    {booking.customer_email}\n"
            f"  Phone:    {booking.customer_phone}\n"
            f"  From:     {booking.pickup_date}\n"
            f"  To:       {booking.dropoff_date}\n"
            f"  Total: €{booking.total_price}\n\n"
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.OWNER_EMAIL],
        fail_silently=False,
    )