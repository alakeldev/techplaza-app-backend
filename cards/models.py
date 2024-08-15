from django.db import models
from django.conf import settings
from cloudinary.models import CloudinaryField

# Create your models here.

class Card(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    profession = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    country = models.CharField(max_length=30)
    photo = CloudinaryField('image', folder='members_cards_images', null=True, blank=True)

    def __str__(self):
        return self.user.email