from datetime import datetime
from django.shortcuts import render
from django.utils import timezone
from .models import Car
from bookings.services import available_cars


def _parse(value):
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


def car_list(request):
    pickup_str = request.GET.get("pickup", "")
    dropoff_str = request.GET.get("dropoff", "")
    pickup = _parse(pickup_str)
    dropoff = _parse(dropoff_str)

    cars = Car.objects.filter(is_available=True)
    searched = False
    error = None

    if pickup_str or dropoff_str:
        if not (pickup_str and dropoff_str):
            error = "Please choose both a pick-up and a drop-off date."
        elif not pickup or not dropoff:
            error = "Please enter valid dates."
        elif pickup < timezone.localdate():
            error = "Pick-up date can't be in the past."
        elif dropoff < pickup:
            error = "The drop-off date can't be before the pick-up date."
        else:
            cars = available_cars(pickup, dropoff)
            searched = True

    return render(request, "fleet/car_list.html", {
        "cars": cars.prefetch_related("photos"),
        "pickup": pickup_str,
        "dropoff": dropoff_str,
        "searched": searched,
        "error": error,
        "today": timezone.localdate().isoformat(),
    })


def contact(request):
    return render(request, "fleet/contact.html")