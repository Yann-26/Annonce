from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from unittest.mock import patch
from annonce.models import creer_annonce


class DashboardViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='admin', password='admin123', is_staff=True, is_superuser=True)
        self.client.login(username='admin', password='admin123')

    @patch('annonce.models.creer_annonce.objects.filter')
    def test_dashboard_view(self, mock_filter):
        mock_filter.return_value = []
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard_admin.html')


class AdminActionsViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='admin', password='admin123', is_staff=True, is_superuser=True)
        self.client.login(username='admin', password='admin123')
        self.annonce = creer_annonce.objects.create(status='pending')

    @patch('annonce.models.creer_annonce.objects.get')
    def test_approve_annonce_view(self, mock_get):
        mock_get.return_value = self.annonce
        response = self.client.post(reverse('approuver_annonce', args=[self.annonce.id]))
        self.assertEqual(response.status_code, 302)  # Check for redirect to dashboard

    # Similarly, write tests for other views like rejeter_annonce, annuler_approbation_annonce, etc.

    def test_user_not_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)  # Check for redirect to login page



