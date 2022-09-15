from urllib import request
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from ..serializers import UserExpenseSerializers, AdminExpenseSerializers
from expense_tracker.models import Expense


class ExpenseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser | IsAuthenticated]

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return AdminExpenseSerializers
        return UserExpenseSerializers

    def get_queryset(self):
        if self.request.user.is_staff:
            return Expense.objects.all()
        return Expense.objects.filter(user=self.request.user)