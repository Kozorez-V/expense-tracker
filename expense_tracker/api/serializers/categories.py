from rest_framework import serializers
from .users import UserSerializers

from expense_tracker.models import Category


class AdminCategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['pk', 'user', 'name']


class UserCategorySerializers(AdminCategorySerializers, serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

