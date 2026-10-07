"""Django settings for MartinBoxes."""

from pathlib import Path
from urllib.parse import urlsplit

from decouple import Csv, config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY", default="")
DEBUG = config("DEBUG", default=False, cast=bool)
ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",
    default="martinboxabl.com,www.martinboxabl.com,localhost,127.0.0.1",
    cast=Csv(),
)
CSRF_TRUSTED_ORIGINS = config(
    "CSRF_TRUSTED_ORIGINS",
    default="https://martinboxabl.com,https://www.martinboxabl.com",
    cast=Csv(),
)

INSTALLED_APPS = [
    "home",
    "search",
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail",
    "modelcluster",
    "taggit",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "django.contrib.sitemaps",
    "django.contrib.postgres",
    "core",
    "emails",
    "shop",
    "blog",
    "dashboard",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"
TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [BASE_DIR / "templates"],
    "APP_DIRS": True,
    "OPTIONS": {"context_processors": [
        "django.template.context_processors.request",
        "django.contrib.auth.context_processors.auth",
        "django.contrib.messages.context_processors.messages",
        "core.context_processors.global_categories",
        "core.context_processors.global_pages",
        "core.context_processors.site_settings",
    ]},
}]
WSGI_APPLICATION = "config.wsgi.application"

DATABASE_URL = config("DATABASE_URL", default="")
DATABASE_SSL_REQUIRE = config("DATABASE_SSL_REQUIRE", default=False, cast=bool)
if DATABASE_URL:
    import dj_database_url

    DATABASES = {"default": dj_database_url.parse(DATABASE_URL, conn_max_age=600, ssl_require=DATABASE_SSL_REQUIRE)}
else:
    DATABASES = {"default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = config("TIME_ZONE", default="UTC")
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}

CLOUDINARY_URL = config("CLOUDINARY_URL", default="")
_cloudinary_url = urlsplit(CLOUDINARY_URL) if CLOUDINARY_URL else None
CLOUDINARY_CLOUD_NAME = config(
    "CLOUDINARY_CLOUD_NAME", default=_cloudinary_url.hostname if _cloudinary_url else ""
)
CLOUDINARY_API_KEY = config(
    "CLOUDINARY_API_KEY", default=_cloudinary_url.username if _cloudinary_url else ""
)
CLOUDINARY_API_SECRET = config(
    "CLOUDINARY_API_SECRET", default=_cloudinary_url.password if _cloudinary_url else ""
)
USE_CLOUDINARY = bool(CLOUDINARY_URL or (CLOUDINARY_CLOUD_NAME and CLOUDINARY_API_KEY and CLOUDINARY_API_SECRET))
if USE_CLOUDINARY:
    try:
        import cloudinary_storage  # noqa: F401
        import cloudinary  # noqa: F401
    except ImportError as exc:
        raise RuntimeError(
            "Cloudinary credentials are configured, but Cloudinary packages are missing. "
            "Run 'pip install -r requirements.txt' in this environment."
        ) from exc
    INSTALLED_APPS += ["cloudinary_storage", "cloudinary"]
    STORAGES["default"] = {"BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage"}
    CLOUDINARY_STORAGE = {
        "CLOUD_NAME": CLOUDINARY_CLOUD_NAME,
        "API_KEY": CLOUDINARY_API_KEY,
        "API_SECRET": CLOUDINARY_API_SECRET,
        "SECURE": True,
        "MEDIA_TAG": "MartinBoxes",
        "PREFIX": "MartinBoxes",
        "INVALID_VIDEO_ERROR_MESSAGE": "Upload a supported video file.",
        "EXCLUDE_DELETE_ORPHANED_MEDIA_PATHS": (),
    }
    MEDIA_URL = f"https://res.cloudinary.com/{CLOUDINARY_CLOUD_NAME}/"
else:
    MEDIA_URL = "/media/"
    MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

WAGTAIL_SITE_NAME = config("SITE_NAME", default="Martin Boxabl")
WAGTAILADMIN_BASE_URL = config("WAGTAILADMIN_BASE_URL", default="http://127.0.0.1:8000")
SITE_ID = 1

RESEND_API_KEY = config("RESEND_API_KEY", default="")
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="Martin Boxabl <martin@martinboxabl.com>")
CONTACT_EMAIL = config("CONTACT_EMAIL", default="support@martinboxabl.com")
SUPPORT_EMAIL = config("SUPPORT_EMAIL", default=CONTACT_EMAIL)
ORDER_EMAIL = config("ORDER_EMAIL", default="orders@martinboxabl.com")

PRODUCTION = config("PRODUCTION", default=not DEBUG, cast=bool)
if PRODUCTION:
    if not SECRET_KEY:
        raise RuntimeError("SECRET_KEY must be set when PRODUCTION is enabled.")
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL must point to the Coolify PostgreSQL service in production.")
    if not USE_CLOUDINARY:
        raise RuntimeError("Configure Cloudinary credentials before running the production site.")
    SECURE_SSL_REDIRECT = config("SECURE_SSL_REDIRECT", default=True, cast=bool)
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = "DENY"
    SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

LOGIN_URL = "/dashboard/login/"
