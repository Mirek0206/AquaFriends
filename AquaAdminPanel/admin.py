from django.db.models import Model

class AquaAdminPanel:
    _registry: list[Model] = []

    def register(self, model: Model):
        ...

    @property
    def registry(self):
        return self._registry