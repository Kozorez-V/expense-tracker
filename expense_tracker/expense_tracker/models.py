from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    date = models.DateField(blank=False, null=False)
    name = models.CharField(max_length=50, blank=False)
    amount = models.FloatField(blank=False, null=False, validators=[MinValueValidator(0.0)])

class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=30, blank=False, unique=True)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                primary_key=True)
    categories = models.ManyToManyField(Category, blank=True)
    limit_flag = models.BooleanField(blank=False, default=False)
    limit = models.PositiveIntegerField(blank=True, null=True)