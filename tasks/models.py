from django.db import models

# Create your models here.

class Task(models.Model):
    task_title = models.CharField(max_length=100)
    task_description = models.CharField(max_length=250)
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return self.task_title