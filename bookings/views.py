from django.shortcuts import render, redirect, get_object_or_404
from .forms import BookingForm
from .models import Booking


def book(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save()
            return redirect("bookings:success", booking_id=booking.id)
    else:
        form = BookingForm()
    return render(request, "bookings/booking_form.html", {"form": form})


def success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, "bookings/success.html", {"booking": booking})