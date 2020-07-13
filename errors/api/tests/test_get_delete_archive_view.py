from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from login.models import User
from errors.models import Error
from errors.api.serializers import ErrorSerializer

class GetDeleteArchiveViewTestCase(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'username',
            'email': 'user@mail.com',
            'password': 'password321',
            'password2': 'password321',
        }
        self.client = APIClient()
        self.url_id_1 = reverse('error_api:error', kwargs={'error_id': 1})
        self.url_id_50 = reverse('error_api:error', kwargs={'error_id': 50})
        
        token = self.client.post(path=reverse('auth_api:register'),
                                data=self.user_data, format='json').data['token']
        self.client.credentials(HTTP_AUTHORIZATION= 'Token ' + token)

        Error.objects.create(title='Error 1', category='DEV',
            level='DEBUG', description='Error Desc 1', address='1.0.0.1',
            user=User.objects.get(pk=1))

    def test_get_error_should_return_200(self):
        r = self.client.get(path=self.url_id_1)
        self.assertEqual(status.HTTP_200_OK, r.status_code)

    def test_get_invalid_error_should_return_404(self):
        r = self.client.get(path=self.url_id_50)
        self.assertEqual(status.HTTP_404_NOT_FOUND, r.status_code)

    def test_get_without_token_should_return_401(self):
        self.client.credentials()
        r = self.client.get(path=self.url_id_1)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, r.status_code)
    
    def test_get_error_data(self):
        serializer = ErrorSerializer(Error.objects.get(pk=1))
        r = self.client.get(path=self.url_id_1)
        self.assertEqual(serializer.data, r.data)

    def test_delete_error_should_return_200(self):
        r = self.client.delete(path=self.url_id_1)
        self.assertEqual(status.HTTP_200_OK, r.status_code)

    def test_delete_invalid_error_should_return_404(self):
        r = self.client.get(path=self.url_id_50)
        self.assertEqual(status.HTTP_404_NOT_FOUND, r.status_code)
    
    def test_delete_without_token_should_return_401(self):
        self.client.credentials()
        r = self.client.delete(path=self.url_id_1)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, r.status_code)

    def test_delete_invalid_token_should_return_401(self):
        self.user_data['username'] ='otheruser'
        self.user_data['email'] = 'otheruser@mail.com'
        token = self.client.post(path=reverse('auth_api:register'),
                                data=self.user_data, format='json').data['token']
        self.client.credentials(HTTP_AUTHORIZATION= 'Token ' + token)

        r = self.client.delete(path=self.url_id_1) 
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, r.status_code)

    def test_archive_error_should_return_200(self):  
        self.assertFalse(Error.objects.get(pk=1).archived)
        r = self.client.put(path=self.url_id_1)
        self.assertEqual(status.HTTP_200_OK, r.status_code)
        self.assertTrue(Error.objects.get(pk=1).archived)
        
    def test_archive_invalid_error_should_return_404(self):
        r = self.client.put(path=self.url_id_50)
        self.assertEqual(status.HTTP_404_NOT_FOUND, r.status_code)

    def test_archive_without_token_should_return_401(self):
        self.client.credentials()
        r = self.client.put(path=self.url_id_1)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, r.status_code)



    

    



        

