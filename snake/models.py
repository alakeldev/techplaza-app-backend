from django.db import models
from accounts.models import User

# Create your models here.

class HighScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()

    def __str__(self):
        return f'{self.user.email} - {self.score}'