from django.test import TestCase
from django.contrib.auth.models import User

from ..models import Category


class UserModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='crown', password='1234pass', email='crown@gmail.com')

    def test_creating_profile(self):
        user = User.objects.get(pk=1)
        self.assertEquals(User.objects.get(profile__user=1), user)

    def test_user_has_default_categories(self):
        self.assertEquals(Category.objects.filter(user=1).count(), 9)
