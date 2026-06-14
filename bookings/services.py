from fleet.models import Car
from .models import Booking

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