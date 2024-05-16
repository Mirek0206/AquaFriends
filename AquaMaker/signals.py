from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import Light, Pump, Heater, Aquarium

@receiver(pre_delete, sender=Light)
def handle_light_deletion(sender, instance, **kwargs):
    default_light = Light.objects.filter(name="Default Light").first()
    if default_light:
        Aquarium.objects.filter(light=instance).update(light=default_light)

@receiver(pre_delete, sender=Pump)
def handle_pump_deletion(sender, instance, **kwargs):
    default_pump = Pump.objects.filter(name="Default Pump").first()
    if default_pump:
        Aquarium.objects.filter(pump=instance).update(pump=default_pump)

@receiver(pre_delete, sender=Heater)
def handle_heater_deletion(sender, instance, **kwargs):
    default_heater = Heater.objects.filter(name="Default Heater").first()
    if default_heater:
        Aquarium.objects.filter(heater=instance).update(heater=default_heater)