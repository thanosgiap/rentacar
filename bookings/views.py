from django.shortcuts import render, redirect, get_object_or_404
from fleet.models import Car
from .forms import BookingForm
from .models import Booking
from .services import send_booking_emails


def book(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save()
            send_booking_emails(booking)        
            return redirect("bookings:success", booking_id=booking.id)
        car_id = request.POST.get("car")
    else:
        car_id = request.GET.get("car")
        initial = {}
        if car_id:
            initial["car"] = car_id
        if request.GET.get("pickup"):
            initial["pickup_date"] = request.GET.get("pickup")
        if request.GET.get("dropoff"):
            initial["dropoff_date"] = request.GET.get("dropoff")
        form = BookingForm(initial=initial)

    cars_data = {
        car.id: {
            "name": car.name,
            "price_per_day": str(car.price_per_day),
            "photo_urls": [photo.image.url for photo in car.photos.all()],
            "category": car.get_category_display(),
            "seats": car.seats,
            "doors": car.doors,
            "luggage": car.luggage,
            "transmission": car.get_transmission_display(),
            "fuel_type": car.get_fuel_type_display(),
            "mileage_km": car.mileage_km,
        }
        for car in Car.objects.prefetch_related("photos")
    }
    return render(request, "bookings/booking_form.html", {
        "form": form,
        "cars_data": cars_data,
    })


def success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, "bookings/success.html", {"booking": booking})
