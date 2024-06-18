from django.db import models
from AquaMaker.models import Aquarium
from django.core.validators import MinValueValidator, MaxValueValidator

class WaterParameter(models.Model):
    aquarium = models.ForeignKey(Aquarium, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    no2 = models.FloatField(validators=[MinValueValidator(0.0)])
    no3 = models.FloatField(validators=[MinValueValidator(0.0)])
    gh = models.FloatField(validators=[MinValueValidator(0.0)])
    kh = models.FloatField(validators=[MinValueValidator(0.0)])
    ph = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(14.0)])

    def __str__(self):
        return f'Parameters for {self.aquarium.name} on {self.date.strftime("%Y-%m-%d")}'

class SituationType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class ExceptionalSituation(models.Model):
    aquarium = models.ForeignKey(Aquarium, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    situation_type = models.ForeignKey(SituationType, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.situation_type.name} in {self.aquarium.name} on {self.date.strftime("%Y-%m-%d")}'
