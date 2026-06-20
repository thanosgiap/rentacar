# RentACar — Project Context

A car-rental booking website for a small 3-car fleet, built with Django.
Customers browse available cars by date, book one, and get an email
confirmation. The owner manages cars and bookings via the Django admin.

## Tech Stack
- Django 6.0 on Python 3.14
- SQLite in development (PostgreSQL planned for production)
- Plain Django templates + one hand-written CSS file (no frontend framework)
- Email via the console backend in development

## Project Structure
- `config/` — settings and root URL config
- `fleet/` — the Car model and the public fleet/search pages
- `bookings/` — the Booking model, availability logic, and booking form
- `templates/` — project-level templates; all extend `base.html`
- `static/css/style.css` — all site styling
- `media/` — uploaded car photos (served only when DEBUG=True)

## Models
- `fleet.Car` — name, category, seats, doors, luggage, transmission,
  fuel_type, mileage_km, price_per_day (Decimal), is_available
- `fleet.CarPhoto` — car (FK, `related_name="photos"`), image, order.
  A car can have any number of photos; `order` controls carousel sequence.
  Managed as an inline on `CarAdmin`, not its own admin page.
- `bookings.Booking` — car (FK), customer_name/email/phone, pickup_date,
  dropoff_date, status (pending/confirmed/cancelled), total_price (Decimal)

## Conventions — follow these
- Business logic lives in `bookings/services.py`, NOT in views.
  Key functions: `is_car_available()`, `available_cars()`, `send_booking_emails()`.
- Availability rule: two date ranges conflict when each starts on or before
  the other ends. Only `pending` and `confirmed` bookings block a car;
  `cancelled` frees it. Same-day handoff counts as a conflict (dates only, no times).
- `Booking.car` uses `on_delete=PROTECT` to preserve booking history —
  never change this to CASCADE.
- `Booking.total_price` is computed in the model's `save()` (days × daily rate,
  minimum 1 day) and stored. Do not recompute it for display.
- All money uses `DecimalField` — never floats.
- Guest booking only: customer details live on the Booking. There are no user accounts.
- Templates extend `templates/base.html`. Use `{% url %}` and `{% static %}`
  tags, never hardcoded paths.
- Prices are shown in euros (€).

## Common Commands
- Run dev server: `python manage.py runserver`
- After model changes: `python manage.py makemigrations` then `python manage.py migrate`
- Create admin user: `python manage.py createsuperuser`
- Django shell: `python manage.py shell`
- Activate venv (Windows / Git Bash): `source venv/Scripts/activate`

## Gotchas
- Uploaded media only serves in development, via the `if settings.DEBUG`
  block in `config/urls.py`.
- Email currently prints to the terminal (console backend); real SMTP is a
  deployment task.
- `SECRET_KEY` and `DEBUG` still live in `settings.py` — move them to
  environment variables before deploying.

## Roadmap (not done yet)
- Content pages: homepage hero, contact/about (phone + WhatsApp), rental terms
- Deployment: PostgreSQL, DEBUG=False, env vars, hosting, domain
- Optional: online payment / deposit (Stripe or Viva Wallet)