from django.contrib.auth.models import User
from rest_framework import serializers

from expense_tracker.models import Category, Expense


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['pk', 'user', 'name']


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk', 'username', 'email']


class ExpenseSerializers(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['pk', 'user', 'category', 'date', 'name', 'amount']
