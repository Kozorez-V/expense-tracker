from rest_framework import serializers

from expense_tracker.models import Expense


class UserExpenseSerializers(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Expense
        fields = ['pk', 'user', 'category', 'date', 'name', 'amount']
        

class AdminExpenseSerializers(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['pk', 'user', 'category', 'date', 'name', 'amount']