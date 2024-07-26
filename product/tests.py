from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from product.models import Category, Product
from product.documents import ProductDocument

class UserRegistrationTests(APITestCase):
    def test_user_registration(self):
        url = reverse('register') 
        data = {
            'username': 'testuser',
            'password': 'password123',
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')

class CategoryModelTests(APITestCase):
    def test_create_category(self):
        data = {
            'title': 'Electronics',
            'description': 'Category for electronic items'
        }
        response = self.client.post(reverse('category-list'), data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Category.objects.filter(title='Electronics').exists())

class ProductModelTests(APITestCase):
    def test_create_product(self):
        category = Category.objects.create(title='Electronics', description='Category for electronic items')
        data = {
            'title': 'Smartphone',
            'price': '299.99',
            'description': 'A new smartphone',
            'category': category.id
        }
        response = self.client.post(reverse('product-list'), data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Product.objects.filter(title='Smartphone').exists())

class SearchViewTests(APITestCase):
    def setUp(self):
     
        category = Category.objects.create(title='Electronics', description='Category for electronic items')
        Product.objects.create(
            title='Smartphone',
            price='299.99',
            description='A new smartphone',
            category=category
        )
        ProductDocument().update(Product.objects.all()) 

    def test_search(self):
        url = reverse('search') 
        response = self.client.get(url, {'q': 'Smartphone'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
        self.assertEqual(response.data[0]['title'], 'Smartphone')
