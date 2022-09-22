from django.test import TestCase
from django.contrib.auth.models import User

from ..models import Category


class UserModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='user', password='1234pass', email='crown@gmail.com')

    def test_creating_profile(self):
        user = User.objects.get(pk=1)
        self.assertEqual(User.objects.get(profile__user=1), user)

    def test_user_has_default_categories(self):
        self.assertEqual(Category.objects.filter(user=1).count(), 9)


class CategoryModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='user', password='1234pass', email='crown@gmail.com')
        Category.objects.create(user=user, name='Одежда')

    def test_string_method(self):
        category = Category.objects.get(pk=10)
        expected_string = 'Одежда'
        self.assertEquals(str(category), expected_string)
