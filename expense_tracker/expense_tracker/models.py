from django.db import models
from django.contrib.auth.models import User

from django.core.validators import MinValueValidator

from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                primary_key=True)
    limit_flag = models.BooleanField(blank=False, default=False)
    limit = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        verbose_name = 'Профили'
        verbose_name_plural = 'Профили'


class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=30, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категории'
        verbose_name_plural = 'Категории'


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateField(blank=False, null=False)
    name = models.CharField(max_length=50, blank=False)
    amount = models.FloatField(blank=False, null=False, validators=[MinValueValidator(0.0)])

    class Meta:
        verbose_name = 'Расходы'
        verbose_name_plural = 'Расходы'
        ordering = ['date', 'category']


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        categories = Category.objects.bulk_create(
            [
                Category(user=instance, name='Дом'),
                Category(user=instance, name='Продукты'),
                Category(user=instance, name='Транспорт'),
                Category(user=instance, name='Здоровье'),
                Category(user=instance, name='Еда вне дома'),
                Category(user=instance, name='Развлечения'),
                Category(user=instance, name='Красота'),
                Category(user=instance, name='Образование'),
                Category(user=instance, name='Домашние животные'),
            ]
        )


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if not instance.is_superuser:
        instance.profile.save()
