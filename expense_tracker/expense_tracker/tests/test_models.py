from datetime import date
from django.test import TestCase
from django.contrib.auth.models import User

from ..models import Category, Expense, Profile


class UserModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='user', password='1234pass', email='user@gmail.com')

    def test_creating_profile(self):
        self.assertEqual(User.objects.get(profile__user=self.user), self.user)

    def test_user_has_default_categories(self):
        self.assertEqual(Category.objects.filter(user=self.user).count(), 9)


class CategoryModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='user', password='1234pass', email='user@gmail.com')
        cls.category = Category.objects.create(user=cls.user, name='Одежда')

    def test_string_method(self):
        expected_string = 'Одежда'
        self.assertEqual(str(self.category), expected_string)

    def test_get_user_categories(self):
        user_categories = Category.objects.filter(user=self.user)
        self.assertEqual(list(Category.objects.get_user_categories(current_user=self.user)), list(user_categories))

class ExpenseModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='user', password='1234pass', email='user@gmail.com')
        cls.category = Category.objects.first()
        cls.expense = Expense.objects.create(user=cls.user, category=cls.category, date=date.today(), name='Покупка', amount=3400)

    def test_user_has_expense(self):
        self.assertEqual(Expense.objects.filter(user=self.user).count(), 1)
    
    def test_category_has_expense(self):
        self.assertEqual(Expense.objects.get(category=self.category), self.expense)


class ProfileModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='user', password='1234pass', email='user@gmail.com')
        cls.profile = Profile.objects.get(user=cls.user)
        cls.profile.day_limit = 1000
        cls.profile.save()

    
    def test_profile_get_limit_value(self):
        self.assertEqual(Profile.objects.filter(user=self.user).get_limit_value(current_user=self.user, limit_time='day_limit'), 1000)