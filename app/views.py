from django.views.generic import ListView
from django.shortcuts import render
from annonce.models import creer_annonce, Commentaire

# Create your views here.

class index(ListView):
    model = creer_annonce
    template_name = 'index.html'
    context_object_name = 'annonces_approuvees' 

    def get_queryset(self):
        return creer_annonce.objects.filter(status='approved')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        annonces_approuvees = context['annonces_approuvees']
        commentaires_par_annonce = {}

        for annonce in annonces_approuvees:
            annonce.debut_promo = annonce.debut_promo.isoformat()
            annonce.fin_promo = annonce.fin_promo.isoformat()
            commentaires_par_annonce[annonce.id] = annonce.commentaires.all()

        context['commentaires_par_annonce'] = commentaires_par_annonce
        return context
