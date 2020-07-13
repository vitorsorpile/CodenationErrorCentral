from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


from errors.models import Error
from errors.api.serializers import ErrorSerializer

class CreateErrorViewTestCase(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'username',
            'email': 'user@mail.com',
            'password': 'password321',
            'password2': 'password321',
        }
        self.client = APIClient()
        self.url = reverse('error_api:create')
        
        token = self.client.post(path=reverse('auth_api:register'),
                                data=self.user_data, format='json').data['token']
        self.client.credentials(HTTP_AUTHORIZATION= 'Token ' + token)

        self.error_data = {
            'title': 'Error 1', 'category': 'DEV',
            'level': 'DEBUG', 'description': 'Error Desc 1',
            'address': '1.0.0.1'
        }
        

    def test_create_error_should_return_201(self):
        r = self.client.post(path=self.url, data=self.error_data)
        self.assertEqual(status.HTTP_201_CREATED, r.status_code)
    
    def test_create_error_without_token_should_return_401(self):
        self.client.credentials()
        r = self.client.post(path=self.url, data=self.error_data)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, r.status_code)    

    def test_create_error_without_title_should_return_400(self):
        self.error_data['title'] = ''
        r = self.client.post(path=self.url, data=self.error_data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, r.status_code)

    def test_create_error_with_invalid_category_should_return_400(self):
        self.error_data['category'] = 'category'
        r = self.client.post(path=self.url, data=self.error_data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, r.status_code)

    def test_create_error_with_invalid_level_should_return_400(self):
        self.error_data['level'] = 'level'
        r = self.client.post(path=self.url, data=self.error_data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, r.status_code) 

    def test_create_error_without_description_should_return_400(self):
        self.error_data['description'] = ''
        r = self.client.post(path=self.url, data=self.error_data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, r.status_code)

    def test_create_error_without_address_should_return_400(self):
        self.error_data['address'] = ''
        r = self.client.post(path=self.url, data=self.error_data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, r.status_code)  

    def test_create_error_get_response_data(self):
        r = self.client.post(path=self.url, data=self.error_data)
        self.assertEqual(ErrorSerializer(Error.objects.get(pk=1)).data, r.data)
