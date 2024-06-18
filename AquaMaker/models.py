from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from simple_history.models import HistoricalRecords


class Pump(models.Model):
    power = models.PositiveSmallIntegerField(default=10)
    min_volume = models.PositiveSmallIntegerField(default=20)
    max_volume = models.PositiveSmallIntegerField(default=40)

    def __str__(self):
        return f'Pump {self.power}W'

class Light(models.Model):
    power = models.PositiveSmallIntegerField(default=10)
    min_volume = models.PositiveSmallIntegerField(default=20)
    max_volume = models.PositiveSmallIntegerField(default=40)

    def __str__(self):
        return f'Light {self.power}W'

class Heater(models.Model):
    power = models.PositiveSmallIntegerField(default=10)
    min_volume = models.PositiveSmallIntegerField(default=20)
    max_volume = models.PositiveSmallIntegerField(default=40)

    def __str__(self):
        return f'Heater {self.power}W'

class Filter(models.Model):
    type = models.CharField(max_length=50)

    def __str__(self):
        return f'Filtr ({self.type})'
    
class Decorator(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'Filter ({self.name})'

class Aquarium(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    x = models.FloatField(validators=[MinValueValidator(10.0)])
    y = models.FloatField(validators=[MinValueValidator(10.0)])
    z = models.FloatField(validators=[MinValueValidator(10.0)])
    light = models.ForeignKey('Light', on_delete=models.CASCADE)
    pump = models.ForeignKey('Pump', on_delete=models.CASCADE)
    heater = models.ForeignKey('Heater', on_delete=models.CASCADE)
    filters = models.ManyToManyField(Filter, blank=True)
    history = HistoricalRecords(m2m_fields=[filters])
    decorators = models.ManyToManyField(Decorator, blank=True)

    def __str__(self) -> str:
        return str(self.name)
