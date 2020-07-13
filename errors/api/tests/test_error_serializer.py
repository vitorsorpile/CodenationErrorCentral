from django.test import TestCase

from errors.api.serializers import ErrorSerializer, SimpleErrorSerializer
from login.models import User
from errors.models import Error

class ErrorSerializerTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username='user',
                                email='user@mail.com',
                                password='password123')

        self.data = {
            'title': 'Error Title',
            'category': 'DEV',
            'level': 'DEBUG',
            'archived': False,
            'description': 'Error Description',
            'address': '1.0.0.1',
        }

        error_data = self.data
        error_data['events'] = 10
        error_data['user'] = user
        self.error = Error.objects.create(**error_data)
        self.serializer_data = ErrorSerializer(self.error).data

    def test_serializer_should_contain_all_fields(self):
        fields = ['id','title', 'category', 'level', 'archived',
                'description', 'address', 'date', 'events', 'email'
        ]
        self.assertEqual(set(fields), set(self.serializer_data.keys()))

    def test_serializer_data(self):
        expected = {}
        expected['id'] = 1
        expected.update(self.data)
        expected['date'] = str(Error.objects.get(pk=1).date)
        expected['events'] = 10
        expected['email'] = 'user@mail.com'
        del expected['user']

        self.assertEqual(sorted(expected), sorted(self.serializer_data))


class SimpleErrorSerializerTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username='user',
                                email='user@mail.com',
                                password='password123')

        self.data = {
            'title': 'Error Title',
            'category': 'DEV',
            'level': 'DEBUG',
            'description': 'Error Description',
            'address': '1.0.0.1',
            'user': user
        }
        error = Error.objects.create(**self.data) 

        self.serializer = SimpleErrorSerializer(instance=error).data

    def test_serializer_should_contain_all_fields(self):
        fields = ['id', 'title', 'category', 'level',
                    'address', 'date', 'events'
            ]
        self.assertEqual(set(fields), self.serializer.keys())
               