from django import forms
from django.utils import timezone
from .models import Booking
from .services import is_car_available


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            "car",
            "customer_name",
            "customer_email",
            "customer_phone",
            "pickup_date",
            "dropoff_date",
        ]
        widgets = {
            "pickup_date": forms.DateInput(attrs={"type": "date"}),
            "dropoff_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        today = timezone.localdate().isoformat()
        self.fields["pickup_date"].widget.attrs["min"] = today
        self.fields["dropoff_date"].widget.attrs["min"] = today

    def clean(self):
        cleaned = super().clean()
        car = cleaned.get("car")
        pickup = cleaned.get("pickup_date")
        dropoff = cleaned.get("dropoff_date")

        if pickup and pickup < timezone.localdate():
            raise forms.ValidationError("Pickup date can't be in the past.")

        if pickup and dropoff:
            if dropoff < pickup:
                raise forms.ValidationError(
                    "Drop-off date can't be before the pickup date."
                )
            if car and not is_car_available(car, pickup, dropoff):
                raise forms.ValidationError(
                    "Sorry, that car is already booked for those dates. "
                    "Please pick different dates or another car."
                )
        return cleaned