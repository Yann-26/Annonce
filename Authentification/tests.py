from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class RegisterTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')

    def test_register_user(self):
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'Test@1234',
            'password_confirm': 'Test@1234'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 302)  # verifier la redirection
        self.assertRedirects(response, reverse('index'))  # verifier la redirection vers'index'
        self.assertEqual(User.objects.count(), 1)  # verifier si l'utilisateur a été crée
        self.assertEqual(User.objects.get().username, 'testuser')  # verifier l'utilisateur est correct

    def test_register_user_passwords_dont_match(self):
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'Test@1234',
            'password_confirm': 'Test@12345'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 302)  # verifier la redirection 
        self.assertRedirects(response, reverse('register'))  # verifier la redirection vers 'register'
        self.assertEqual(User.objects.count(), 0)  # verifier si l'utilisateur n'a pas été crée

    def test_register_user_username_taken(self):
        User.objects.create(username='testuser', email='testuser@example.com', password='Test@1234')
        data = {
            'username': 'testuser',
            'email': 'testuser2@example.com',
            'password': 'Test@1234',
            'password_confirm': 'Test@1234'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 302)  # verifier la  redirection
        self.assertRedirects(response, reverse('register'))  # verifier la redirection vers 'register'
        self.assertEqual(User.objects.count(), 1)  # verifier qu'un autre utilisateur n'a pas été crée quand même

    def test_register_user_email_taken(self):
        User.objects.create(username='testuser', email='testuser@example.com', password='Test@1234')
        data = {
            'username': 'testuser2',
            'email': 'testuser@example.com',
            'password': 'Test@1234',
            'password_confirm': 'Test@1234'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 302)  # Check redirection
        self.assertRedirects(response, reverse('register'))  # verifier la redirection vers 'register'
        self.assertEqual(User.objects.count(), 1)  # verifier qu'un autre utilisateur n'a pas été crée quand même


class SigninTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('signin')
        self.test_user = User.objects.create_user(username='assiri', password='assiri@1234')

    def test_signin_user(self):
        data = {
            'username': 'assiri',
            'password': 'assiri@1234'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 302)  # verifier la  redirection
        self.assertRedirects(response, reverse('index'))  # verifier la redirection vers 'index'
        self.assertEqual(int(self.client.session['_auth_user_id']), self.test_user.pk)  # verifier que l'utilisateur est bien connecté

    def test_signin_user_faaux_password(self):
        data = {
            'username': 'testuser',
            'password': 'fauxpassword'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 200 )  # verifier la redirection
        # self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.login_url)  # verifier la redirectio vers 'signin'
        self.assertNotIn('_auth_user_id', self.client.session)  # verifier si l'utilisateur n'est pas connecté
        


class SignoutTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.logout_url = reverse('signout')
        self.test_user = User.objects.create_user(username='testuser', password='Test@1234')

    def test_signout_user(self):
        self.client.login(username='testuser', password='Test@1234')
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)  # verifier la redirection
        self.assertRedirects(response, reverse('index'))  # # verifier la redirection vers 'index'
        self.assertNotIn('_auth_user_id', self.client.session)  # verifier que l'utilisateur est bien deconnecté
