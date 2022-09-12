from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from ..serializers import CategorySerializers, UserSerializers, ExpenseSerializers
from expense_tracker.models import Category, Expense


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers

    @action(methods=['get'], detail=True)
    def categories(self, request, pk=None):
        categories = Category.objects.filter(user__pk=pk)
        return Response({'categories': [category.name for category in categories]})


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializers
