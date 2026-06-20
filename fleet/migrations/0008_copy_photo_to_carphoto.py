from django.db import migrations


def copy_photos_forward(apps, schema_editor):
    Car = apps.get_model("fleet", "Car")
    CarPhoto = apps.get_model("fleet", "CarPhoto")
    for car in Car.objects.exclude(photo="").exclude(photo__isnull=True):
        CarPhoto.objects.create(car=car, image=car.photo, order=0)


def copy_photos_backward(apps, schema_editor):
    Car = apps.get_model("fleet", "Car")
    CarPhoto = apps.get_model("fleet", "CarPhoto")
    for car in Car.objects.all():
        first_photo = CarPhoto.objects.filter(car=car).order_by("order", "id").first()
        if first_photo:
            car.photo = first_photo.image
            car.save(update_fields=["photo"])


class Migration(migrations.Migration):

    dependencies = [
        ("fleet", "0007_add_carphoto"),
    ]

    operations = [
        migrations.RunPython(copy_photos_forward, copy_photos_backward),
    ]
