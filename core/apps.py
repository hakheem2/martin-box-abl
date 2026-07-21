from django.apps import AppConfig
from django.db.models.signals import post_migrate

def run_create_superuser(sender, **kwargs):
    from .utils import create_superuser
    try:
        create_superuser()
    except Exception as e:
        print(f"Error creating superuser: {e}")

class CoreConfig(AppConfig):
    name = "core"
    
    def ready(self):
        # This hooks into the post_migrate signal.
        # It will only run AFTER migrations have completed successfully.
        post_migrate.connect(run_create_superuser, sender=self)