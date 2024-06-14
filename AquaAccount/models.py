from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    GENDER_CHOICES = [
        ("M", "Mężczyzna"),
        ("K", "Kobieta"),
    ]

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True, editable=False
    )
    is_active = models.BooleanField(default=False)
    bio = models.CharField(max_length=1500, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    phone_number = models.CharField(max_length=40, null=True, blank=True)
    profile_image = models.ImageField(upload_to='profiles', null=True, blank=True, default='profiles/user-default.png')
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(18), MaxValueValidator(125)], null=True, blank=True)

    def __str__(self) -> str:
        return str(self.user)

    @property
    def imageURL(self):
        try:
            url = self.profile_image.url
        except Exception:
            url = ''
        return url