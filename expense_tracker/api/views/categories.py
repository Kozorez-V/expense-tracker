from rest_framework import generics, viewsets

from ..serializers import CategoriesSerializers
from expense_tracker.models import Category


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializers
