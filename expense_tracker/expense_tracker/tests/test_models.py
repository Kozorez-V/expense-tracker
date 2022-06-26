from django.test import TestCase
from expense_tracker.models import Category

class CategoryTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(
            user='',
            expense='',
            name='Продукты'
        )

    def test_it_has_information_fields(self):
        self.assertIsInstance(self.category.name, str)

