from django.test import TestCase

from login.api.serializers import RegisterSerializer


class RegisterSerializerTestCase(TestCase):
    def setUp(self):
        self.data = {
            'username': 'user',
            'email': 'useremail@mail.com',
            'password': 'userpassword123',
            'password2': 'userpassword123'
        }

    def test_serializer_is_valid(self):
        serializer = RegisterSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_is_invalid_empty_username(self):
        self.data['username'] = ''
        serializer = RegisterSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())

    def test_serializer_is_invalid_empty_email(self):
        self.data['email'] = ''
        serializer = RegisterSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
    
    def test_serializer_is_invalid_empty_password(self):
        self.data['password'] = ''
        serializer = RegisterSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
    
    def test_serializer_is_invalid_empty_password2(self):
        self.data['password2'] = ''
        serializer = RegisterSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
