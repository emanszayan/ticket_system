from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from customer.models import Customer
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomerAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpassword", is_superuser=True)
        self.client.force_authenticate(user=self.user)  # Authenticate requests

        self.customer_data = {
            'name': 'John Doe',
            'mobile': '1234567890',
            'phone': '0987654321',
            'email': 'john@example.com',
            'address': '123 Street, City'
        }
        self.customer = Customer.objects.create(**self.customer_data, created_by=self.user)

    def test_create_customer(self):
        response = self.client.post('/api/v1/customer/create', self.customer_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['created_by'], self.user)  # Verify created_by is set correctly

    def test_get_customers(self):
        response = self.client.get('/api/v1/customer/list')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_customer(self):
        response = self.client.get(f'/api/v1/customer/{self.customer.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_customer(self):
        updated_data = {
            'name': 'Jane Doe',
            'mobile': '1112223333',
            'phone': '4445556666',
            'email': 'jane@example.com',
            'address': '456 Avenue, City'
        }
        print(self.customer.id)
        response = self.client.put(f'/api/v1/customer/update/{self.customer.id}', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['created_by'], self.user.id)  # Ensure created_by remains the same

    def test_delete_customer(self):
        response = self.client.delete(f'/api/v1/customer/delete/{self.customer.id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
