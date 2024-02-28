from django.urls import path
from . import views


urlpatterns = [
    path('creer/annonce/', views.create_annonce, name="annonce"),
    path('commenter/annonce/<int:annonce_id>/', views.ajouter_commentaire, name='ajouter_commentaire'),
]