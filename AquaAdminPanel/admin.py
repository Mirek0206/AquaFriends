from django.db.models import Model

class AquaAdminPanel:
    _instance = None
    _registry: dict[str, Model] = dict()

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = super(AquaAdminPanel, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def register(self, model: Model):
        self._registry[model.__name__] = model

    @property
    def registry(self) -> dict[str, Model]:
        return self._registry