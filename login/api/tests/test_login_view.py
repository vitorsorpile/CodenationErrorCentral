from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class LoginViewTestCase(TestCase):
    def setUp(self):
        self.data = {
            'username': 'useremail@mail.com',
            'password': 'userpassword123',
        }
        self.client = APIClient()
        self.url = reverse('auth_api:login')
        self.client.post(path=reverse('auth_api:register'),
                        data={'username': 'user',
                        'email': 'useremail@mail.com',
                        'password': 'userpassword123',
                        'password2': 'userpassword123'},
                        format='json')

    def test_valid_login_should_return_200(self):
        r = self.client.post(self.url, data=self.data, format='json')
        self.assertEqual(status.HTTP_200_OK, r.status_code)

    def test_not_registered_login_should_return_400(self):
        self.data['username'] = 'u@mail.com'
        r = self.client.post(self.url, data=self.data, format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, r.status_code)

    def test_wrong_password_login_should_return_400(self):
        self.data['password'] = 'anything'
        r = self.client.post(self.url, data=self.data, format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, r.status_code)
