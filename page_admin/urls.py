from django.urls import path
from . import views

urlpatterns = [
    path('administrateur/dashboard/', views.dashboard, name='dashboard'),
    path('approuver-annonce/<int:annonce_id>/', views.approuver_annonce, name='approuver_annonce'),
    path('rejeter-annonce/<int:annonce_id>/', views.rejeter_annonce, name='rejeter_annonce'),
    path('remettre-en-attente/<int:annonce_id>/', views.remettre_en_attente_annonce, name='remettre_en_attente'),
    path('reapprouver-annonce/<int:annonce_id>/', views.approuver_a_nouveau_annonce, name='reapprouver'),
    path('annuler-approbation/<int:annonce_id>/', views.annuler_approbation_annonce, name='rannuler_approbation'),
    path('suppression-annonce/<int:annonce_id>/', views.supprimer_annonce, name='suppression'),
]
