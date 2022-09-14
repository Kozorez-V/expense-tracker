from rest_framework import serializers

from expense_tracker.models import Category


class UserCategorySerializers(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Category
        fields = ['pk', 'user', 'name']


class AdminCategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['pk', 'user', 'name']

