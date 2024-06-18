from django.apps import AppConfig


class AquamakerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'AquaMaker'

    def ready(self) -> None:
        import AquaMaker.signals  # noqa: F401
