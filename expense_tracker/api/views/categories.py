from rest_framework import generics

from ..serializers import CategoriesSerializers
from expense_tracker.models import Category


class CategoriesAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializers
