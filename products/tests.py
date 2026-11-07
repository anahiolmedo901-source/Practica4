from django.test import TestCase
from unittest.mock import patch
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


class AuthenticationAndIntegrationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.password = 'Mercado-Verde-8247!X'
        self.user = User.objects.create_user(
            email='persona@example.test',
            password=self.password,
            first_name='Persona',
            last_name='Prueba',
            phone='662-555-0101',
        )

    def _login(self, email='persona@example.test', password=None):
        return self.client.post('/api/token/', {
            'email': email,
            'password': password or self.password,
        }, format='json')

    def test_registration_jwt_profile_and_openapi_hide_password(self):
        created = self.client.post('/api/v1/users/', {
            'email': 'registro@example.test',
            'first_name': 'Nueva',
            'last_name': 'Cuenta',
            'phone': '662-555-0102',
            'password': 'Cerezo-Seguro-9362!Q',
        }, format='json')
        self.assertEqual(created.status_code, 201)
        self.assertNotIn('password', created.data)

        token_response = self._login()
        self.assertEqual(token_response.status_code, 200)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token_response.data['access']}")
        profile = self.client.get('/api/v1/me/')
        self.assertEqual(profile.status_code, 200)
        self.assertEqual(profile.data['phone'], '662-555-0101')
        self.assertNotIn('password', profile.data)

        schema = self.client.get('/swagger/openapi.json')
        self.assertEqual(schema.status_code, 200)
        schema_data = schema.json()
        self.assertEqual(schema_data['info']['title'], 'Mercado Local API')
        self.assertTrue(schema_data['components']['schemas']['User']['properties']['password']['writeOnly'])
        self.assertIn('/api/v1/soap/numero-a-letras/', schema_data['paths'])

    def test_staff_patch_without_password_keeps_existing_password(self):
        target = User.objects.create_user(
            email='objetivo@example.test', password='Objetivo-Anterior-847!Z', phone='662-000-0000'
        )
        staff_password = 'Staff-Seguro-847!Z'
        staff = User.objects.create_user(
            email='staff@example.test', password=staff_password, is_staff=True
        )
        self.client.force_authenticate(user=staff)
        response = self.client.patch(
            f'/api/v1/users/{target.id}/', {'phone': '662-111-1111'}, format='json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotIn('password', response.data)
        target.refresh_from_db()
        self.assertTrue(target.check_password('Objetivo-Anterior-847!Z'))
        self.assertFalse(target.check_password(staff_password))

    def test_regular_user_cannot_list_or_edit_other_accounts(self):
        another = User.objects.create_user(email='otra@example.test', password='Otra-Cuenta-847!Z')
        self.client.force_authenticate(user=self.user)
        self.assertEqual(self.client.get('/api/v1/users/').status_code, 403)
        self.assertEqual(
            self.client.patch(f'/api/v1/users/{another.id}/', {'first_name': 'Cambio'}).status_code,
            403,
        )
        self.assertEqual(self.client.get('/api/v1/me/').status_code, 200)

    @patch('products.views.number_to_words', return_value='forty-two')
    def test_soap_endpoint_requires_jwt_and_returns_service_result(self, mock_number_to_words):
        self.assertEqual(self.client.get('/api/v1/soap/numero-a-letras/?numero=42').status_code, 401)
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/v1/soap/numero-a-letras/?numero=42')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['numero'], 42)
        self.assertEqual(response.data['resultado'], 'forty-two')
        mock_number_to_words.assert_called_once_with(42)

        invalid = self.client.get('/api/v1/soap/numero-a-letras/?numero=fuera-de-rango')
        self.assertEqual(invalid.status_code, 400)
