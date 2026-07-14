# Bò Nhúng Giấm Ngày Xưa — Restaurant Website

Django web app for a Vietnamese restaurant: public menu and news, guest/customer ordering, staff order portal, and bilingual UI (Vietnamese / English).

## Features

- **Public site** — homepage, menu, news feeds, cart, checkout
- **Accounts** — signup (with phone), login, profile, order history
- **Orders** — guest or logged-in cart, order confirmation, staff workflow
- **Staff portal** — order management, status pipeline, reports (superuser), CSV export
- **i18n** — VI default; EN via nav language switch. Menu **names stay Vietnamese**; descriptions and news **content** translate (manual `*_en` fields or auto-translate fallback)
- **Roles** — customer, staff, manager, superuser

## Requirements

- Python 3.11+ (tested on 3.13)
- pip

## Quick start

```bash
# Clone and enter project
cd restaurant_website

# Virtual environment
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS/Linux

# Dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt   # optional: locale compilation

# Environment
copy .env.example .env            # Windows
# cp .env.example .env            # macOS/Linux
# Edit .env — set SECRET_KEY, ADMIN_CANCEL_CODE, etc.

# Database
python manage.py migrate

# Admin user
python manage.py createsuperuser

# (Optional) Logo — add static/images/logonew.jpg

# (Optional) Auto-fill English descriptions for existing menu/news
python manage.py translate_content

# Run
python manage.py runserver
```

Open http://127.0.0.1:8000/

## Environment variables

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Django secret key (required in production) |
| `DEBUG` | `True` / `False` |
| `ALLOWED_HOSTS` | Comma-separated hosts |
| `ADMIN_CANCEL_CODE` | Code required for non-manager staff to cancel orders (optional) |

See [.env.example](.env.example).

## Translations

**UI strings** (buttons, nav, labels):

```bash
# After editing locale/*/LC_MESSAGES/django.po or scripts/generate_locale.py
python scripts/generate_locale.py
pybabel compile -d locale -D django
```

**Menu / news content:**

- Names and news titles always display in Vietnamese.
- Add **Description (English)** / **Content (English)** when creating items, or run:

```bash
python manage.py translate_content
python manage.py translate_content --dry-run   # preview only
```

## User roles

Set in Django admin on `CustomUser`:

| Role | Access |
|------|--------|
| Customer | Browse, cart, checkout, profile, order history |
| Staff | Staff order dashboard |
| Manager | Staff + add/edit menu & news (skip cancel code) |
| Superuser | Full admin + sales reports |

## Project layout

```
accounts/           Custom user, auth, profile
restaurant_site/    Homepage, menu, news
orders/             Cart, checkout, staff portal
templates/          HTML templates
static/             CSS, JS, images
locale/             VI/EN UI translations
scripts/            generate_locale.py helper
```

## Production notes

- Set `DEBUG=False` and a strong `SECRET_KEY`
- Use a production database (PostgreSQL recommended)
- Configure a real `EMAIL_BACKEND` for password reset
- Run `python manage.py collectstatic`
- Use HTTPS and update `ALLOWED_HOSTS` / `CSRF_TRUSTED_ORIGINS` in settings

## Tests

```bash
python manage.py test accounts orders
```
