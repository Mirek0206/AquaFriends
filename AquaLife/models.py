from django.core.validators import MinValueValidator
from django.db import models
from simple_history.models import HistoricalRecords

from AquaMaker.models import Aquarium


class Species(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Fish(models.Model):
    name = models.CharField(max_length=50)
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(0)])
    species = models.ForeignKey(Species, on_delete=models.CASCADE)
    aquarium = models.ForeignKey(Aquarium, on_delete=models.CASCADE)
    date_added = models.DateField(auto_now_add=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.name

