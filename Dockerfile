FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential curl libpq-dev libjpeg62-turbo-dev zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./requirements.txt
RUN python -m pip install --upgrade pip \
    && python -m pip install -r requirements.txt

COPY . .

# Static collection only needs Django settings. These are build-only values;
# production secrets and service URLs must be injected by Coolify at runtime.
RUN SECRET_KEY=build-only-not-a-production-secret DEBUG=False PRODUCTION=False \
    python manage.py collectstatic --noinput

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=90s --retries=3 \
    CMD curl --fail --silent --show-error --header 'Host: 127.0.0.1' --header 'X-Forwarded-Proto: https' http://127.0.0.1:8000/health/ || exit 1

# This project is deployed as one web container. Migrations run before Gunicorn.
CMD ["sh", "-c", "python manage.py migrate --noinput && exec gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 3 --access-logfile - --error-logfile -"]
