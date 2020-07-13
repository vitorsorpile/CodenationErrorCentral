from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from login.models import User
from errors.models import Error
from errors.api.serializers import ErrorSerializer

class ListErrorsViewTestCase(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'username',
            'email': 'user@mail.com',
            'password': 'password321',
            'password2': 'password321',
        }
        self.client = APIClient()
        self.url = reverse('error_api:list')

        token = self.client.post(path=reverse('auth_api:register'),
                                data=self.user_data, format='json').data['token']
        self.client.credentials(HTTP_AUTHORIZATION= 'Token ' + token)

        category_options = ['PRODUÇÃO', 'DEV', 'HOMOLOGAÇÃO']
        level_options = ['ERROR', 'WARNING', 'DEBUG']
        for i in range(4):
            Error.objects.create(title=f'Error {i}', category=category_options[i%3],
                    level=level_options[i%3], description=f'Error Desc {i}', address='1.0.0.1',
                    events=i, user=User.objects.get(pk=1))

        Error.objects.create(title='Random Title', category='DEV',
                level='ERROR', description=f'Random Desc', address='12.1.1.1',
                events=4, user=User.objects.get(pk=1))

        Error.objects.create(title='Random Extra Title', category='DEV',
                level='DEBUG', description=f'Random Extra Desc', address='12.1.1.1',
                events=5, user=User.objects.get(pk=1))
    
    def test_get_filter_should_return_200(self):
        r = self.client.get('/api/error/list?category=DEV', format='json')
        self.assertEqual(status.HTTP_200_OK, r.status_code)

    def test_get_filter_category_DEV_should_return_3_errors(self):
        r = self.client.get('/api/error/list?category=DEV', format='json')
        self.assertEqual(3, r.data['count'])

    def test_get_filter_category_PRODUCAO_should_return_2_errors(self):
        r = self.client.get('/api/error/list?category=PRODUÇÃO', format='json')
        self.assertEqual(2, r.data['count'])

    def test_get_filter_category_HOMOLOGACAO_should_return_2_errors(self):
        r = self.client.get('/api/error/list?category=HOMOLOGAÇÃO', format='json')
        self.assertEqual(1, r.data['count'])

    def test_get_order_should_return_200(self):
        r = self.client.get('/api/error/list?category=DEV&orderBy=level', format='json')
        self.assertEqual(status.HTTP_200_OK, r.status_code)

    def test_get_order_by_level(self):
        sequence = ['DEBUG', 'ERROR', 'WARNING']
        r = self.client.get('/api/error/list?category=DEV&orderBy=level', format='json')
        r_sequence = [error['level'] for error in r.data['results']]
        self.assertSequenceEqual(sequence, r_sequence)

    def test_get_order_by_events(self):
        sequence = [5, 4, 1]
        r = self.client.get('/api/error/list?category=DEV&orderBy=-events', format='json')
        r_sequence = [error['events'] for error in r.data['results']]
        self.assertSequenceEqual(sequence, r_sequence)  

    def test_get_search_should_return_200(self):
        r = self.client.get('/api/error/list?search=Random&searchBy=title', format='json')
        self.assertEqual(status.HTTP_200_OK, r.status_code)

    def test_get_search_by_title_should_return_2_logs(self):
        r = self.client.get('/api/error/list?search=Random&searchBy=title', format='json')
        self.assertEqual(2, r.data['count'])

    def test_get_search_by_title_should_return_4_logs(self):
        r = self.client.get('/api/error/list?search=error&searchBy=title', format='json')
        self.assertEqual(4, r.data['count'])

    def test_get_search_by_description_should_return_1_log(self):
        r = self.client.get('/api/error/list?search=Random+Extra&searchBy=description', format='json')
        self.assertEqual(1, r.data['count'])

    def test_get_search_by_description_should_return_4_logs(self):
        r = self.client.get('/api/error/list?search=error&searchBy=description', format='json')
        self.assertEqual(4, r.data['count'])

    def test_get_search_by_address_should_return_2_logs(self):
        r = self.client.get('/api/error/list?search=12.1.1.1&searchBy=address', format='json')
        self.assertEqual(2, r.data['count'])

    def test_get_search_by_address_should_return_4_logs(self):
        r = self.client.get('/api/error/list?search=1.0.0.1&searchBy=address', format='json')
        self.assertEqual(4, r.data['count'])
