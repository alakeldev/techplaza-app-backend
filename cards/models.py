from django.db import models
from accounts.models import User 

# Create your models here.

class Card(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    profession = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    country = models.CharField(max_length=30)

    def __str__(self):
        return self.user.email