from django.db import models
from AquaMaker.models import Aquarium

class SituationType(models.Model):
    name = models.CharField(max_length=50)
    hint = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class ExceptionalSituation(models.Model):
    aquarium = models.ForeignKey(Aquarium, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    situation_type = models.ForeignKey(SituationType, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.situation_type.name} in {self.aquarium.name} on {self.date.strftime("%Y-%m-%d")}'