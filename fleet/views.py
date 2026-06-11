from django.shortcuts import render
from .models import Car


def car_list(request):
    cars = Car.objects.all()
    return render(request, "fleet/car_list.html", {"cars": cars})