import stripe

from fleet.models import Car
from .models import Booking
from django.conf import settings
from django.core.mail import send_mail

stripe.api_key = settings.STRIPE_SECRET_KEY

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

def create_checkout_session(booking, success_url, cancel_url):
    """Create a Stripe Checkout Session for an unpaid booking and return it."""
    session = stripe.checkout.Session.create(
        mode="payment",
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "eur",
                "product_data": {
                    "name": f"{booking.car.name} rental "
                            f"({booking.pickup_date} → {booking.dropoff_date})",
                },
                "unit_amount": int(booking.total_price * 100),
            },
            "quantity": 1,
        }],
        customer_email=booking.customer_email,
        success_url=success_url,
        cancel_url=cancel_url,
        metadata={"booking_id": str(booking.id)},
    )
    booking.stripe_session_id = session.id
    booking.save()
    return session


def send_booking_emails(booking):
    if booking.payment_method == "card":
        payment_line = "Payment received — you're all set, no need to pay again."
    else:
        payment_line = f"You'll pay €{booking.total_price} directly at pickup."

    # Confirmation to the customer
    send_mail(
        subject="Your RentACar booking is confirmed",
        message=(
            f"Hi {booking.customer_name},\n\n"
            f"Thank you for booking with RentACar! Here are your details:\n\n"
            f"  Car:   {booking.car.name}\n"
            f"  From:  {booking.pickup_date}\n"
            f"  To:    {booking.dropoff_date}\n"
            f"  Total: €{booking.total_price}\n\n"
            f"{payment_line}\n\n"
            f"Need anything or have a question? Call us at {settings.OWNER_PHONE}.\n\n"
            f"See you soon!\nRentACar"
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[booking.customer_email],
        fail_silently=False,
    )

    # Alert to the owner
    payment_status = "Paid online by card" if booking.is_paid else "Will pay at pickup"
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
            f"  Total:    €{booking.total_price}\n"
            f"  Payment:  {payment_status}\n\n"
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.OWNER_EMAIL],
        fail_silently=False,
    )