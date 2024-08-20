from django.db import models
from accounts.models import User


class Task(models.Model):
    """
    Model representing a task created by a user.
    """

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )
    task_title = models.CharField(max_length=100)
    task_description = models.CharField(max_length=250)
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return self.task_title
