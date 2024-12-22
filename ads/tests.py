# tests.py

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Service, ServiceCategory
from .forms import ServiceForm

# Model Tests
class ServiceTisementModelTests(TestCase):

    def test_service_creation(self):
        user = User.objects.create_user(username='testuser', password='password')
        service = Service.objects.create(
            ads_author=user,
            title='Test Service',
            description='Test description',
            occupation='Electrician',
            contact_info='1234567890'
        )
        self.assertEqual(service.title, 'Test Service')
        self.assertEqual(service.description, 'Test description')

    def test_service_category_creation(self):
        category = ServiceCategory.objects.create(name='Plumbing')
        self.assertEqual(category.name, 'Plumbing')

    def test_user_creation(self):
        user = User.objects.create_user(username='newuser', password='password')
        self.assertEqual(user.username, 'newuser')


# View Tests
class ServiceViewsTests(TestCase):

    def test_service_list_view(self):
        user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('service_list'))  # Assuming you have this URL name
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Service')

    def test_service_creation_view(self):
        user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('add_service'), {
            'title': 'New Service',
            'description': 'New service description',
            'occupation': 'Plumber',
            'contact_info': '9876543210',
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertRedirects(response, reverse('service_list'))  # Redirect after successful creation

    def test_service_edit_view(self):
        user = User.objects.create_user(username='testuser', password='password')
        service = Service.objects.create(
            ads_author=user,
            title='Old Service',
            description='Old description',
            occupation='Plumber',
            contact_info='1234567890'
        )
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('edit_service', kwargs={'pk': service.pk}), {
            'title': 'Updated Service',
            'description': 'Updated description',
            'occupation': 'Electrician',
            'contact_info': '1231231234',
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success
        service.refresh_from_db()
        self.assertEqual(service.title, 'Updated Service')

    def test_service_delete_view(self):
        user = User.objects.create_user(username='testuser', password='password')
        service = Service.objects.create(
            ads_author=user,
            title='Service to delete',
            description='Service description',
            occupation='Electrician',
            contact_info='1231231234'
        )
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('delete_service', kwargs={'pk': service.pk}))
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertFalse(Service.objects.filter(pk=service.pk).exists())  # Ensure it's deleted


# Form Tests
class ServiceFormTests(TestCase):

    def test_form_valid(self):
        form_data = {
            'title': 'Valid Service',
            'description': 'Description of service',
            'occupation': 'Electrician',
            'contact_info': '9876543210',
        }
        form = ServiceForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        form_data = {
            'title': '',
            'description': 'Missing title',
            'occupation': 'Plumber',
            'contact_info': '1234567890',
        }
        form = ServiceForm(data=form_data)
        self.assertFalse(form.is_valid())


# Integration Tests
class IntegrationTests(TestCase):

    def test_full_service_workflow(self):
        # Register a new user
        user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        
        # Add a new service
        response = self.client.post(reverse('add_service'), {
            'title': 'Test Service',
            'description': 'Test service description',
            'occupation': 'Plumber',
            'contact_info': '9876543210',
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success
        
        # Check service appears in the list
        response = self.client.get(reverse('service_list'))
        self.assertContains(response, 'Test Service')

        # Edit the service
        service = Service.objects.get(title='Test Service')
        response = self.client.post(reverse('edit_service', kwargs={'pk': service.pk}), {
            'title': 'Updated Service',
            'description': 'Updated description',
            'occupation': 'Electrician',
            'contact_info': '1231231234',
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success
        service.refresh_from_db()
        self.assertEqual(service.title, 'Updated Service')


# Error Handling Tests
class ErrorPageTests(TestCase):
    
    def test_404_page(self):
        response = self.client.get('/non-existing-page/')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')

    def test_500_page(self):
        response = self.client.get('/trigger-500/')
        self.assertEqual(response.status_code, 500)
