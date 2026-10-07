# MartinBoxes

Django storefront and Wagtail CMS for MartinBoxes.

## Local setup

1. Create a virtual environment and install `requirements.txt`.
2. Copy `.env.example` to `.env`, set `SECRET_KEY`, and set `DEBUG=True` for local development.
3. Run `python manage.py migrate` and `python manage.py createsuperuser`.
4. Run `python manage.py runserver`.

The custom, responsive site dashboard is available at `/dashboard/` (sign in at `/dashboard/login/`). It includes site settings, staff user management, blog post drafting and publishing with cover image uploads, and full product management for homes, including pricing, categories, images, gallery photos, specifications, and visibility. Products with customer orders cannot be deleted, preserving order history; they can be deactivated instead. The Django admin remains available at `/admin/` for advanced maintenance, and Wagtail content editing is available at `/cms/`.

## Coolify deployment

Set `DEBUG=False`, `PRODUCTION=True`, `SECRET_KEY`, `ALLOWED_HOSTS`, and `CSRF_TRUSTED_ORIGINS` in Coolify. Production refuses to start unless PostgreSQL and Cloudinary are configured, so it cannot silently fall back to ephemeral SQLite or local media. For PostgreSQL, set either `DATABASE_URL` or all of `DB_NAME`, `DB_USER`, `DB_PASSWORD`, and `DB_HOST`; `DB_PORT` defaults to `5432`. Use the Coolify PostgreSQL service's internal hostname and port, not a public endpoint. Coolify PostgreSQL normally uses `DATABASE_SSL_REQUIRE=False`; set it to `True` only if your database requires TLS.

For persistent uploads, configure Cloudinary using `CLOUDINARY_URL` or `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, and `CLOUDINARY_API_SECRET`. Uploads are stored under the Cloudinary `MartinBoxes/` prefix, then organized by media type (for example, `MartinBoxes/homes/` and `MartinBoxes/categories/`). Install dependencies with `pip install -r requirements.txt` so `django-cloudinary-storage` is available when Cloudinary is enabled. For notifications, set `RESEND_API_KEY` and the verified sender in `DEFAULT_FROM_EMAIL`. Contact messages go to `SUPPORT_EMAIL` and order requests go to `ORDER_EMAIL`; both have Martin Boxabl defaults and can be overridden in Coolify.

The repository includes a root `Dockerfile` and no longer uses the old Railway Procfile. In Coolify, set **Build Pack** to **Dockerfile**, **Base Directory** to `/`, **Dockerfile Location** to `Dockerfile`, and **Ports Exposes** to `8000`. Leave the start command on the Dockerfile default. The image installs `requirements.txt` (including Cloudinary), collects static assets, then runs database migrations before Gunicorn starts. The container exposes `/health/` for health checks and honors Coolify's `PORT` variable.

After deploying the blog content, open the web service terminal in Coolify and run `python manage.py seed_blog_posts`. This idempotent command creates or refreshes four published, image-backed guides, their categories and tags, and the blog index if needed. It uses the image files included in `static/images/`; the posts then appear on the home page and at `/blog/`.

In Coolify's Environment Variables settings, mark secrets and application configuration **Runtime only** (Build time unavailable, Runtime available). The Dockerfile does not need credentials to build: static collection uses temporary build-only Django settings. Set `SECRET_KEY`, `DEBUG=False`, `PRODUCTION=True`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, `DATABASE_URL` or `DB_NAME`, `DB_USER`, `DB_PASSWORD`, and `DB_HOST` (plus optional `DB_PORT`), `DATABASE_SSL_REQUIRE`, Cloudinary credentials, `RESEND_API_KEY`, `DEFAULT_FROM_EMAIL`, `SUPPORT_EMAIL`, `ORDER_EMAIL`, and `WAGTAILADMIN_BASE_URL`. Do not paste live secrets into `.env.example` or build arguments. Make sure the deployed branch includes these Dockerfile changes before redeploying.

Create the first dashboard user with `python manage.py createsuperuser` in the Coolify container terminal after the first successful deployment. Sign in at `/dashboard/login/`. The container startup applies migrations automatically; deploy one web replica when using startup migrations.

## Site endpoints

- `/sitemap.xml` lists public pages, categories, and active homes.
- `/robots.txt` advertises the sitemap and excludes private/admin paths.
- `/admin/` manages users, shop records, orders, and site-wide settings.
- `/cms/` manages Wagtail blog pages.
