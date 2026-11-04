from django.test import TestCase
from rest_framework.test import APIClient
from .models import Category, Product, User

class CategoryTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Crear usuario de prueba y autenticar
        self.user = User.objects.create_user(email='testuser@example.com', password='test123')
        self.client.force_authenticate(user=self.user)
        # Crear categoría inicial
        self.category = Category.objects.create(name='Electronica')

    def test_create_category(self):
        response = self.client.post('/api/v1/categories/', {'name': 'Ropa'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Category.objects.count(), 2)

    def test_list_categories(self):
        response = self.client.get('/api/v1/categories/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1) 


class ProductTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='testuser2@example.com', password='test123')
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(name='Electronica')
        self.product = Product.objects.create(
            name='Celular',
            category=self.category,
            description='Teléfono Inteligente con super funciones',
            price=8500.00
        )

    def test_create_product(self):
        response = self.client.post('/api/v1/products/', {
            'name': 'Blusa Negra',
            'category': self.category.id,
            'description': 'Blusa Negro de Algodón',
            'price': 350.00
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Product.objects.count(), 2)

    def test_list_products(self):
        response = self.client.get('/api/v1/products/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)  

    def test_update_product(self):
        response = self.client.put(f'/api/v1/products/{self.product.id}/', {
            'name': 'Celular Pro',
            'category': self.category.id,
            'description': 'Teléfono Inteligente actualizado',
            'price': 9500.00
        })
        self.assertEqual(response.status_code, 200)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Celular Pro')

    def test_delete_product(self):
        response = self.client.delete(f'/api/v1/products/{self.product.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Product.objects.count(), 0)

    def test_precio_final_autenticado(self):
        response = self.client.get(f'/api/v1/products/{self.product.id}/precio-final/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('precio_final', response.data)

    def test_precio_final_sin_autenticar(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(f'/api/v1/products/{self.product.id}/precio-final/')
        self.assertEqual(response.status_code, 401)
