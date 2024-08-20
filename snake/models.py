from django.db import models
from accounts.models import User


class HighScore(models.Model):
    """
    Model representing a high score achieved by a user in the Snake game.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()

    def __str__(self):
        return f"{self.user.email} - {self.score}"
