from rest_framework import serializers

from expense_tracker.models import Category


class CategoriesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']
