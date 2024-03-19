from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from annonce.models import creer_annonce, Commentaire
from datetime import datetime
from django.utils import timezone

class TestIndexView(TestCase):
    def setUp(self):
        # Nettoyez la base de données avant de commencer le test
        creer_annonce.objects.all().delete()
        User.objects.all().delete()

        # Créez des annonces et un utilisateur pour les tests
        debut_promo = timezone.make_aware(datetime.strptime('10/11/2021', '%d/%m/%Y'))
        fin_promo = timezone.make_aware(datetime.strptime('10/11/2021', '%d/%m/%Y'))
        utilisateur = User.objects.create_user(username='testuser', password='testpassword')
        creer_annonce.objects.create(modele_voiture='Annonce 1', prix_voiture='10', status='approved', fin_promo=fin_promo, debut_promo=debut_promo)
        creer_annonce.objects.create(modele_voiture='Annonce 2', prix_voiture='20', status='approved', fin_promo=fin_promo, debut_promo=debut_promo)
        creer_annonce.objects.create(modele_voiture='Annonce 3', prix_voiture='30', status='rejected', fin_promo=fin_promo, debut_promo=debut_promo)
        Commentaire.objects.create(utilisateur=utilisateur, annonce=creer_annonce.objects.get(modele_voiture='Annonce 1'), contenu='Commentaire 1')
        Commentaire.objects.create(utilisateur=utilisateur, annonce=creer_annonce.objects.get(modele_voiture='Annonce 1'), contenu='Commentaire 2')
        Commentaire.objects.create(utilisateur=utilisateur, annonce=creer_annonce.objects.get(modele_voiture='Annonce 2'), contenu='Commentaire 3')

    def test_get_index(self):
        # Vérifier que la page d'index s'affiche correctement
        client = Client()
        response = client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

        # Vérifier que seules les annonces approuvées sont affichées
        self.assertEqual(len(response.context['annonces_approuvees']), 2)

        # Vérifier que les commentaires sont associés aux annonces appropriées
        annonce_1 = creer_annonce.objects.get(modele_voiture='Annonce 1')
        annonce_2 = creer_annonce.objects.get(modele_voiture='Annonce 2')
        self.assertEqual(len(annonce_1.commentaires.all()), 2)
        self.assertEqual(len(annonce_2.commentaires.all()), 1)
