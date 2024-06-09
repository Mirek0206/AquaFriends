from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Pump(models.Model):
    power = models.CharField(max_length=50)

    def __str__(self):
        return f'Moc ({self.power})'

class Light(models.Model):
    power = models.CharField(max_length=50)

    def __str__(self):
        return f'Moc ({self.power})'

class Heater(models.Model):
    power = models.CharField(max_length=50)

    def __str__(self):
        return f'Moc ({self.power})'

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
    decorators = models.ManyToManyField(Decorator, blank=True)
    
    def __str__(self) -> str:
        return str(self.name)
