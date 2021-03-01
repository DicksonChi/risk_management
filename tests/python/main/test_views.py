
import uuid
import json

from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from main.constants import FIELD_TYPE_TEXT
from main.models import User, RiskType, Field
from tests.python.main.test_models import UserFactory, FieldFactory, RiskTypeFactory


class UserTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='user@email.com'
        )

    def test_user_does_not_exist(self):
        email = 'test@email.com'
        response = self.client.get(
            reverse('main:find_user', kwargs={'email': email})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_does_exist(self):
        response = self.client.get(
            reverse('main:find_user', kwargs={'email': self.user.email})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("id"), self.user.id)

    def test_add_user(self):
        email = 'test@email.com'
        response = self.client.post(
            reverse('main:register'), data={'email': email}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class RiskTypeTests(TestCase):

    def setUp(self):
        self.field = FieldFactory()
        self.risk_type= RiskTypeFactory()

    def test_get_risk_type_list(self):
        response = self.client.get(
            reverse('main:fetch_all_risk_type', kwargs={'user_id': self.risk_type.user.id})
        )
        self.assertEqual(response.data.get("code"), "010")
        self.assertEqual(isinstance(response.data.get("risk_types"), list), True)

    def test_add_risk_type(self):
        user = self.risk_type.user.id
        # create with existing field
        response = self.client.post(
            reverse('main:add_risk_type'),
            json.dumps({
                'user': str(user),
                'name': "Automobile Risk",
                'fields': [
                    {
                        'id': str(self.field.id),
                        'name': self.field.name,
                        'field_type': self.field.field_type
                    }
                ]
            }),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("code"), "010")
        risk_type = RiskType.objects.latest('date_added')
        self.assertEqual(risk_type.name, "Automobile Risk")
        self.assertEqual(Field.objects.count(), 1)

    def test_add_risk_type_wrong_field_id(self):
        user = self.risk_type.user.id
        # create with existing field
        response = self.client.post(
            reverse('main:add_risk_type'),
            json.dumps({
                'user': str(user),
                'name': "Automobile Risk",
                'fields': [
                    {
                        'id': str(uuid.uuid4()),
                        'name': "New Field",
                        'field_type': FIELD_TYPE_TEXT
                    }
                ]
            }),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("code"), "010")
        self.field.refresh_from_db()
        risk_type = RiskType.objects.latest('date_added')
        self.assertEqual(risk_type.name, "Automobile Risk")
        self.assertEqual(Field.objects.count(), 2)
        # fetch single risk type
        response = self.client.get(
            reverse('main:fetch_single_risk_type', kwargs={'id': self.risk_type.id})
        )
        self.assertEqual(response.data.get("code"), "010")
        self.assertEqual(isinstance(response.data.get("risk_types"), list), False)

        response = self.client.get(
            reverse('main:fetch_all_risk_type', kwargs={'user_id': self.risk_type.user.id})
        )
        self.assertEqual(response.data.get("code"), "010")
        self.assertEqual(isinstance(response.data.get("risk_types"), list), True)

    def test_add_risk_type_no_field_id(self):
        user = self.risk_type.user.id
        # create with existing field
        response = self.client.post(
            reverse('main:add_risk_type'),
            json.dumps({
                'user': str(user),
                'name': "Automobile Risk",
                'fields': [
                    {
                        'name': "New Field",
                        'field_type': FIELD_TYPE_TEXT
                    }
                ]
            }),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("code"), "010")
        self.field.refresh_from_db()
        risk_type = RiskType.objects.latest('date_added')

        self.assertEqual(risk_type.name, "Automobile Risk")
        self.assertEqual(Field.objects.count(), 2)

    def test_update_risk_type_no_field_id(self):
        # create with wrong id
        response = self.client.put(
            reverse('main:update_single_risk_type', kwargs={'id': uuid.uuid4()}),
            json.dumps({
                'name': "Automobile Risk",
                'fields': [
                    {
                        'id': str(self.field.id),
                        'name': self.field.name,
                        'field_type': self.field.field_type
                    }
                ]
            }),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # create with existing field
        response = self.client.put(
            reverse('main:update_single_risk_type', kwargs={'id': self.risk_type.id}),
            json.dumps({
                'name': "Automobile Risk",
                'fields': [
                    {
                        'id': str(self.field.id),
                        'name': self.field.name,
                        'field_type': self.field.field_type
                    }
                ]
            }),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("code"), "010")
        risk_type = RiskType.objects.last()
        self.assertEqual(risk_type.fields.first().name, self.field.name)
        self.assertEqual(Field.objects.count(), 1)


class FieldTests(TestCase):

    def setUp(self):
        self.user = UserFactory()

    def test_get_field_list(self):
        response = self.client.get(
            reverse('main:fetch_all_field', kwargs={})
        )
        self.assertEqual(response.data.get("code"), "010")
        self.assertEqual(isinstance(response.data.get("fields"), list), True)

    def test_add_risk_field(self):
        # create with existing field
        response = self.client.post(
            reverse('main:add_field'), data={
                'name': "Test Field",
                'field_type': FIELD_TYPE_TEXT,
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("code"), "010")
        self.assertEqual(Field.objects.count(), 1)
