from django.apps import AppConfig


class AquaaccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'AquaAccount'

    def ready(self):
        import AquaAccount.signals
