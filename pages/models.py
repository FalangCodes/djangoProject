from django.db import models
from django.contrib.auth.models import User
    
class Budget(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)

class Expense(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50)
    date = models.DateField()
