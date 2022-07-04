# Generated by Django 4.0.5 on 2022-07-04 08:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('expense_tracker', '0023_alter_category_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='expense',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='categories',
        ),
        migrations.AddField(
            model_name='category',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='expense',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='expense_tracker.category'),
        ),
    ]