from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone

# Create your views here.


def create_annonce(request):
    if request.method  == "POST":
        annonce = request.POST.get('annonce')
        marque_voiture = request.POST.get('marque_voiture')
        prix_voiture = request.POST.get('prix_voiture')
        modele_voiture = request.POST.get('modele_voiture')
        body_style = request.POST.get('body_style')
        color  = request.POST.get('color')
        debut_promo = request.POST.get('debut_promo')
        fin_promo = request.POST.get('fin_promo')
        description = request.POST.get('description')
        type = request.POST.get('type')
        photo_voiture = request.POST.get('photo_voiture')
        
        
        new_annonce = creer_annonce(
            annonce = annonce,
            marque_voiture = marque_voiture,
            prix_voiture = prix_voiture,
            modele_voiture = modele_voiture,
            body_style = body_style,
            color = color,
            debut_promo = debut_promo,
            fin_promo = fin_promo,
            description = description,
            type = type,
            photo_voiture = photo_voiture,
        )
        # annonce.created_by = request.user
        new_annonce.save()
        messages.success(request, 'Votre annonce a été créée avec succès. En attente de validation par l\'administrateur')
        return redirect('index')
        
    datas = {}
    return render(request, 'Annonce.html', datas)



@login_required
def ajouter_commentaire(request, annonce_id ):
    if request.method == 'POST':
        contenu = request.POST.get('contenu')  
        utilisateur = request.user 

        annonce = creer_annonce.objects.get(pk=annonce_id)  
        
        # Créer le commentaire
        commentaire = Commentaire(
            annonce=annonce,
            utilisateur=utilisateur,
            contenu=contenu,
            date_creation=timezone.now()
        )
        commentaire.save()

        return redirect('index')  

   