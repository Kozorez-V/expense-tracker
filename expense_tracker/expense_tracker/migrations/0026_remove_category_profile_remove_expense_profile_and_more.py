# Generated by Django 4.0.5 on 2022-07-04 08:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('expense_tracker', '0025_remove_category_user_remove_expense_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='profile',
        ),
        migrations.RemoveField(
            model_name='expense',
            name='profile',
        ),
        migrations.AddField(
            model_name='category',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='expense',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]