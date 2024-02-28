from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver


# Create your models here.

class creer_annonce(models.Model):
    annonce = models.CharField(max_length=30)
    marque_voiture = models.CharField(max_length=50)
    modele_voiture = models.CharField(max_length=50)
    prix_voiture = models.BigIntegerField()
    body_style = models.CharField(max_length=50)
    color  = models.CharField(max_length=50)
    debut_promo = models.DateTimeField(auto_now_add=False)
    fin_promo = models.DateTimeField(auto_now_add=False)
    description = models.CharField(max_length=150)
    type = models.CharField(max_length=10)
    photo_voiture = models.ImageField(upload_to='annonces/')
    # created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('annonce_achieve', 'annonce_achieve'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    #STANDARDS
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    @classmethod
    def get_user_announcements(cls, user_id):
        return cls.objects.filter(user_id=user_id)

    def approuver_annonce(self):
        self.status = 'approved'
        self.save()

    def rejecter_annonce(self):
        self.status = 'rejected'
        self.save()

    def remettre_en_attente(self):
        self.status = 'pending'
        self.save()

    def annuler_approbation(self):
        if self.status == 'approved':
            self.status = 'pending'
            self.save()
        else:
            pass  

    def reapprouver(self):
        if self.status == 'rejected':
            self.status = 'approved'
            self.save()
        elif self.status == 'pending':
            self.status = 'approved'
            self.save()
        else:
            pass 
    
    def check_and_update_status(self):
        if self.status == 'approved' and self.fin_promo < timezone.now():
            self.status = 'annonce_achieve'
            self.fin_promo = timezone.now() + timezone.timedelta(days=30)  
            self.save()

    def __str__(self):
        return self.annonce
    

@receiver(pre_save, sender=creer_annonce)
def update_annonce_status(sender, instance, **kwargs):
    instance.check_and_update_status()



class Commentaire(models.Model):
    annonce = models.ForeignKey('creer_annonce', related_name='commentaires', on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    contenu = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commentaire de {self.utilisateur.username} sur l'annonce {self.annonce.id}"
