import factory
from django.test import TestCase

from main.constants import FIELD_TYPE_TEXT
from main.models import User, Field, RiskType, Risk


class UserFactory(factory.django.DjangoModelFactory):
    email = 'test@email.com'

    class Meta:
        model = User


class FieldFactory(factory.django.DjangoModelFactory):
    name = 'Test Field'
    field_type = FIELD_TYPE_TEXT

    class Meta:
        model = Field


class RiskTypeFactory(factory.django.DjangoModelFactory):
    name = 'Test Risk'
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = RiskType


class RiskFactory(factory.django.DjangoModelFactory):
    name = 'Test Risk'
    risk_type = factory.SubFactory(RiskTypeFactory)

    class Meta:
        model = Risk


class UserModelsTests(TestCase):
    def setUp(self):
        self.user = UserFactory.create(email='test@test.com')

    def test_unicode(self):
        self.assertEqual(str(self.user), 'test@test.com')

    def test_super_user(self):
        super_user = User.objects.create_superuser(email='email@test.com')
        self.assertEqual(super_user.is_superuser, True)

    def test_user(self):
        user = User.objects.create_user(email='email@test.com')
        self.assertEqual(user.is_superuser, False)
