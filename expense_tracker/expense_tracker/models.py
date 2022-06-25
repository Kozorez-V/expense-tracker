from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Profile(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                primary_key=True)
    limit = models.PositiveIntegerField(blank=True, null=True)

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    date = models.DateField(blank=False, null=False)
    name = models.CharField(max_length=50, blank=False)
    amount = models.FloatField(blank=False, null=False, validators=[MinValueValidator(0.0)])

class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=30, blank=False)