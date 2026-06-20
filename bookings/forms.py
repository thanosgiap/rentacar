import re

from django import forms
from django.utils import timezone
from .models import Booking
from .services import is_car_available

# Accepts an optional leading "+" (country code / extension) plus digits,
# spaces, dashes and parentheses, e.g. "+30 690 1234567" or "+1 (555) 123-4567".
PHONE_FORMAT_RE = re.compile(r"^\+?[0-9\s\-()]+$")
PHONE_MIN_DIGITS = 8
PHONE_MAX_DIGITS = 15  # ITU E.164 international maximum, country code included


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            "car",
            "pickup_date",
            "dropoff_date",
            "customer_name",
            "customer_email",
            "customer_phone",
            "payment_method",
        ]
        widgets = {
            "pickup_date": forms.DateInput(attrs={"type": "date"}),
            "dropoff_date": forms.DateInput(attrs={"type": "date"}),
            "customer_phone": forms.TextInput(attrs={"placeholder": "690 1234567"}),
            "payment_method": forms.RadioSelect,
        }

    def clean_customer_phone(self):
        phone = self.cleaned_data["customer_phone"].strip()
        if not PHONE_FORMAT_RE.match(phone):
            raise forms.ValidationError(
                "Enter a valid phone number, e.g. +30 690 1234567."
            )
        digit_count = len(re.sub(r"\D", "", phone))
        if not (PHONE_MIN_DIGITS <= digit_count <= PHONE_MAX_DIGITS):
            raise forms.ValidationError(
                f"Phone number must be {PHONE_MIN_DIGITS} to {PHONE_MAX_DIGITS} digits, "
                "including the country code."
            )
        return phone

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