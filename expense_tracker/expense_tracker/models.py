from datetime import date

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                primary_key=True, verbose_name='Пользователь')
    limit = models.PositiveIntegerField(blank=True, null=True, verbose_name='Лимит')

    class Meta:
        verbose_name = 'Профили'
        verbose_name_plural = 'Профили'

    def limit_flag(self):
        return self.objects.limit > 0


class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='Пользователь')
    name = models.CharField(max_length=30, blank=False, verbose_name='Название')

    class Meta:
        verbose_name = 'Категории'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class ExpenseQuerySet(models.QuerySet):
    def today(self, current_user):
        return self.filter(date=date.today(), user=current_user)

    def current_week(self, current_user):
        return self.filter(date__week=date.today().isocalendar()[1],
                           user=current_user)

    def current_year(self, current_user):
        return self.filter(date__year=date.today().isocalendar()[0],
                           user=current_user)


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='Пользователь')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=False, verbose_name='Категория')
    date = models.DateField(blank=False, null=False, verbose_name='Дата')
    name = models.CharField(max_length=50, blank=False, verbose_name='Название')
    amount = models.FloatField(blank=False, null=False, validators=[MinValueValidator(1.0)], verbose_name='Сумма')
    objects = ExpenseQuerySet.as_manager()

    class Meta:
        verbose_name = 'Расходы'
        verbose_name_plural = 'Расходы'
        ordering = ['-date', 'category']


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
