from datetime import date
from django.test import TestCase
from django.contrib.auth.models import User

from ..models import Category, Expense, Profile


class UserModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='user', password='1234pass', email='user@gmail.com')

    def test_creating_profile(self):
        user = User.objects.get(pk=1)
        self.assertEqual(User.objects.get(profile__user=1), user)

    def test_user_has_default_categories(self):
        self.assertEqual(Category.objects.filter(user=1).count(), 9)


class CategoryModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='user', password='1234pass', email='user@gmail.com')
        Category.objects.create(user=user, name='Одежда')

    def test_string_method(self):
        category = Category.objects.get(pk=10)
        expected_string = 'Одежда'
        self.assertEqual(str(category), expected_string)

    def test_get_user_categories(self):
        user = User.objects.get(pk=1)
        user_categories = Category.objects.filter(user=user)
        self.assertEqual(Category.objects.get_user_categories(current_user=user), user_categories)


class ExpenseModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='user', password='1234pass', email='user@gmail.com')
        category = Category.objects.get(pk=1)
        Expense.objects.create(user=user, category=category, date=date.today(), name='Покупка', amount=3400)

    def test_user_has_expense(self):
        self.assertEqual(Expense.objects.filter(user=1).count(), 1)
    
    def test_category_has_expense(self):
        expense = Expense.objects.get(pk=1)
        self.assertEqual(Expense.objects.get(category=1), expense)


class ProfileModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='user', password='1234pass', email='user@gmail.com')
        profile = Profile.objects.get(user=user)
        profile.day_limit = 1000
        profile.save()

    
    def test_profile_get_limit_value(self):
        user = User.objects.get(pk=1)
        self.assertEqual(Profile.objects.filter(user=user).get_limit_value(current_user=user, limit_time='day_limit'), 1000)
