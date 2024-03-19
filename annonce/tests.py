from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import creer_annonce, Commentaire


class TestCreateAnnonceView(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.annonce_data = {
            'annonce': 'Test annonce',
            'marque_voiture': 'Test marque',
            'modele_voiture': 'Test modele',
            'prix_voiture': '10000',
            'body_style': 'Test style',
            'color': 'Test couleur',
            'debut_promo': '2023-03-01',
            'fin_promo': '2023-03-31',
            'description': 'Test description',
            'type': 'vente',
            'photo_voiture': 'tests/files/test_image.jpg'
        }

    def test_create_annonce_not_logged_in(self):
        response = self.client.get(reverse('annonce'))
        self.assertRedirects(response, '/Authentification/register/?next=/creer/annonce/')

    def test_create_annonce_logged_in(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('annonce'))
        self.assertEqual(response.status_code, 302)

    def test_create_annonce_form_valid(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('annonce'), data=self.annonce_data)
        self.assertRedirects(response, reverse('index'))
        self.assertEqual(creer_annonce.objects.count(), 1)
        self.assertEqual(creer_annonce.objects.first().annonce, 'Test annonce')

    def test_create_annonce_form_invalid(self):
        self.client.login(username='testuser', password='testpassword')
        annonce_data_invalid = {
            'annonce': '',
            'marque_voiture': '',
            'modele_voiture': '',
            'prix_voiture': '',
            'body_style': '',
            'color': '',
            'debut_promo': '',
            'fin_promo': '',
            'description': '',
            'type': '',
            'photo_voiture': ''
        }
        response = self.client.post(reverse('annonce'), data=annonce_data_invalid)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'annonce', 'Ce champ est obligatoire.')
        self.assertFormError(response, 'form', 'marque_voiture', 'Ce champ est obligatoire.')
        self.assertFormError(response, 'form', 'modele_voiture', 'Ce champ est obligatoire.')
        self.assertFormError(response, 'form', 'prix_voiture', 'Ce champ est obligatoire.')
        self.assertFormError(response, 'form', 'body_style', 'Ce champ est obligatoire.')
        self.assertFormError(response, 'form', 'color', 'Ce champ est obligatoire.')
        self.assertFormError(response, 'form', 'debut_promo', 'Ce champ est obligatoire.')
        self.assertFormError(response, 'form', 'fin_promo', 'Ce champ est obligatoire.')
        self.assertFormError(response, 'form', 'description', 'Ce champ est obligatoire.')
        self.assertFormError(response, 'form', 'type', 'Ce champ est obligatoire.')
        self.assertEqual(creer_annonce.objects.count(), 0)


class TestAddCommentView(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.annonce = creer_annonce.objects.create(
            annonce='Test annonce',
            marque_voiture='Test marque',
            modele_voiture='Test modele',
            prix_voiture=10000,
            body_style='Test style',
            color='Test couleur',
            debut_promo='2023-03-01',
            fin_promo='2023-03-31',
            description='Test description',
            type='vente',
            photo_voiture='tests/files/test_image.jpg',
            created_by=self.user
        )
        self.commentaire_data = {
            'contenu': 'Test commentaire'
        }

    def test_ajouter_commentaire_not_logged_in(self):
        response = self.client.post(reverse('ajouter_commentaire', args=[self.annonce.id]), data=self.commentaire_data)
        self.assertRedirects(response, '/Authentification/register/?next=/ajouter_commentaire/' + str(self.annonce.id) + '/')

    def test_ajouter_commentaire_logged_in(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('ajouter_commentaire', args=[self.annonce.id]), data=self.commentaire_data)
        self.assertRedirects(response, reverse('index'))
        self.assertEqual(Commentaire.objects.count(), 1)
        self.assertEqual(Commentaire.objects.first().contenu, 'Test commentaire')
        self.assertEqual(Commentaire.objects.first().annonce, self.annonce)
        self.assertEqual(Commentaire.objects.first().utilisateur, self.user)