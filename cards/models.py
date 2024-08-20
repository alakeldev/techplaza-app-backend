from django.db import models
from accounts.models import User


class Card(models.Model):
    """
    Model representing a user's card with contact and professional information.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    profession = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    country = models.CharField(max_length=30)

    def __str__(self):
        return self.user.email
