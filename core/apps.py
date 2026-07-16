from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = "core"

    def ready(self):
        from .utils import create_superuser

        try:
            create_superuser()
        except Exception as e:
            print(e)