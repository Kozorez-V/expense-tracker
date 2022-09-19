from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from ..serializers import UserExpenseSerializers, AdminExpenseSerializers
from expense_tracker.models import Expense


class ExpenseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser | IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['pk', 'user', 'category', 'date', 'name', 'amount']
    ordering_fields = ['pk', 'user', 'category', 'date', 'name', 'amount']

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return AdminExpenseSerializers
        return UserExpenseSerializers

    def get_queryset(self):
        if self.request.user.is_staff:
            return Expense.objects.all()
        return Expense.objects.filter(user=self.request.user)