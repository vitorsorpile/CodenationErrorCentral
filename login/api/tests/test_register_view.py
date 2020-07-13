from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class RegisterViewTestCase(TestCase):
    def setUp(self):
        self.data = {
            'username': 'user',
            'email': 'useremail@mail.com',
            'password': 'userpassword123',
            'password2': 'userpassword123'
        }
        self.client = APIClient()
        self.url = reverse('auth_api:register')

    def test_register_user_should_return_201(self):
        r = self.client.post(self.url, data=self.data, format='json')
        self.assertEqual(status.HTTP_201_CREATED, r.status_code)

    def test_register_existing_user_should_return_400(self):
        self.client.post(self.url, data=self.data, format='json')
        r = self.client.post(self.url, data=self.data, format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, r.status_code)

    def test_register_user_without_username_should_return_400(self):
        self.data['username'] = ''
        r = self.client.post(self.url, data=self.data, format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, r.status_code)

    def test_register_user_without_email_should_return_400(self):
        self.data['email'] = ''
        r = self.client.post(self.url, data=self.data, format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, r.status_code)
    
    def test_register_user_without_password_should_return_400(self):
        self.data['password'] = ''
        r = self.client.post(self.url, data=self.data, format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, r.status_code)
    
    def test_register_user_without_password2_should_return_400(self):
        self.data['password2'] = ''
        r = self.client.post(self.url, data=self.data, format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, r.status_code)
        
    def test_register_user_with_different_passwords_should_return_400(self):
        self.data['password2'] = 'anything'
        r = self.client.post(self.url, data=self.data, format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, r.status_code)
        