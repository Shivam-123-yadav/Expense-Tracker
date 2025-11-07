from django.db import models

# Create your models here.
from django.utils import timezone

class Expense(models.Model):
    category = models.CharField(max_length=200)
    amount = models.FloatField()
    descriptions = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.category} - {self.amount}'
    