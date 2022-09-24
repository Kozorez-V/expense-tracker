from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Category, Expense, Profile

class setUpMixins:
    def setUp(self):
        self.client = Client()
        self.test_user = User.objects.create_user(username='user', password='1234pass', email='user@gmail.com')
        self.test_user.is_superuser = False
        self.test_user.is_active = True
        self.test_user.save()
        login = self.client.login(username='user', password='1234pass')
        self.failUnless(login, 'Could not log in')

class IndexTest(setUpMixins, TestCase):
    def test_url_exist(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'expense_tracker/index.html')


class ShowCategoriesTest(setUpMixins, TestCase):
    def test_url_exist(self):
        response = self.client.get(reverse('categories'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('categories'))
        self.assertTemplateUsed(response, 'expense_tracker/category_list.html')

    def test_pagination_is_correct(self):
        response = self.client.get(reverse('categories'))
        self.assertTrue('is_paginated' in response.context)
        self.assertEqual(len(response.context['categories']), 9)

    def test_view_has_title(self):
        response = self.client.get(reverse('categories'))
        self.assertTrue('title' in response.context)


class ExpenseHistoryTest(setUpMixins, TestCase):
    def test_url_exist(self):
        response = self.client.get(reverse('expense_history'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('expense_history'))
        self.assertTemplateUsed(response, 'expense_tracker/expense_history.html')

    def test_pagination_is_correct(self):
        response = self.client.get(reverse('expense_history'))
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue('expenses' in response.context)

    def test_view_has_title(self):
        response = self.client.get(reverse('expense_history'))
        self.assertTrue('title' in response.context)