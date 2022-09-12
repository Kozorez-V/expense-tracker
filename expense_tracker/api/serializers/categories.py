from django.contrib.auth.models import User
from rest_framework import serializers

from expense_tracker.models import Category, Expense, Profile


class CategorySerializers(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Category
        fields = ['pk', 'user', 'name']


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk', 'username', 'email']


class ExpenseSerializers(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Expense
        fields = ['pk', 'user', 'category', 'date', 'name', 'amount']


class ProfileSerializers(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Profile
        fields = ['user', 'day_limit', 'week_limit', 'month_limit']
