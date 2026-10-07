# MartinBoxes

Django storefront and Wagtail CMS for MartinBoxes.

## Local setup

1. Create a virtual environment and install `requirements.txt`.
2. Copy `.env.example` to `.env`, set `SECRET_KEY`, and set `DEBUG=True` for local development.
3. Run `python manage.py migrate` and `python manage.py createsuperuser`.
4. Run `python manage.py runserver`.

The custom, responsive site dashboard is available at `/dashboard/` (sign in at `/dashboard/login/`). It includes site settings, staff user management, blog post drafting and publishing with cover image uploads, and full product management for homes, including pricing, categories, images, gallery photos, specifications, and visibility. Products with customer orders cannot be deleted, preserving order history; they can be deactivated instead. The Django admin remains available at `/admin/` for advanced maintenance, and Wagtail content editing is available at `/cms/`.

## Coolify deployment

Set `DEBUG=False`, `PRODUCTION=True`, `SECRET_KEY`, `ALLOWED_HOSTS`, and `CSRF_TRUSTED_ORIGINS` in the Coolify application environment. Set `DATABASE_URL` to the attached PostgreSQL service URL. The application uses PostgreSQL when `DATABASE_URL` is present and SQLite only for local development.

For persistent uploads, configure Cloudinary using `CLOUDINARY_URL` or `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, and `CLOUDINARY_API_SECRET`. Uploads are stored under the Cloudinary `MartinBoxes/` prefix, then organized by media type (for example, `MartinBoxes/homes/` and `MartinBoxes/categories/`). Install dependencies with `pip install -r requirements.txt` so `django-cloudinary-storage` is available when Cloudinary is enabled. For notifications, set `RESEND_API_KEY` and the verified sender in `DEFAULT_FROM_EMAIL`. Contact messages go to `SUPPORT_EMAIL` and order requests go to `ORDER_EMAIL`; both have Martin Boxabl defaults and can be overridden in Coolify.

Configure Coolify to run `python manage.py migrate` as a pre-deploy command and start the web service with:

```sh
gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 3 --access-logfile - --error-logfile -
```

Create the first dashboard user with `python manage.py createsuperuser` (or run `createsuperuser` in the Coolify shell). Admin users can then add additional users and edit the single Site Settings record from the Django admin.

## Site endpoints

- `/sitemap.xml` lists public pages, categories, and active homes.
- `/robots.txt` advertises the sitemap and excludes private/admin paths.
- `/admin/` manages users, shop records, orders, and site-wide settings.
- `/cms/` manages Wagtail blog pages.
