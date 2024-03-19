from django.shortcuts import get_object_or_404, render, redirect
from annonce.models import creer_annonce
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages


def est_administrateur(user):
    return  user.is_superuser


@user_passes_test(est_administrateur)
def dashboard(request):
    annonces_en_attente = creer_annonce.objects.filter(status='pending')
    annonces_approuvees = creer_annonce.objects.filter(status='approved')
    annonces_rejetees = creer_annonce.objects.filter(status='rejected')
    annonces_achieve = creer_annonce.objects.filter(status='annonce_achieve')
    datas = {
        'annonces_en_attente': annonces_en_attente,
        'annonces_approuvees' : annonces_approuvees,
        'annonces_rejetees' : annonces_rejetees,
        'annonces_achieve' : annonces_achieve
    }
    return render(request, 'dashboard_admin.html', datas)


@user_passes_test(est_administrateur)
def approuver_annonce(request, annonce_id):
    annonce = get_object_or_404(creer_annonce, id=annonce_id)
    annonce.approuver_annonce()
    return redirect('dashboard')


@user_passes_test(est_administrateur)
def rejeter_annonce(request, annonce_id):
    annonce = get_object_or_404(creer_annonce, id=annonce_id)
    annonce.rejecter_annonce()
    return redirect('dashboard')


@user_passes_test(est_administrateur)
def annuler_approbation_annonce(request, annonce_id):
    annonce = get_object_or_404(creer_annonce, id=annonce_id)
    annonce.annuler_approbation()
    return redirect('dashboard')


@user_passes_test(est_administrateur)
def remettre_en_attente_annonce(request, annonce_id):
    annonce = get_object_or_404(creer_annonce, id=annonce_id)
    annonce.remettre_en_attente()
    return redirect('dashboard')


@user_passes_test(est_administrateur)
def approuver_a_nouveau_annonce(request, annonce_id):
    annonce = get_object_or_404(creer_annonce, id=annonce_id)
    annonce.reapprouver()  
    return redirect('dashboard')


@user_passes_test(est_administrateur)
def supprimer_annonce(request, annonce_id):
    annonce = get_object_or_404(creer_annonce, id=annonce_id)
    try:
        annonce.delete()
        messages.success(request, "Annonce supprimée avec succès.")
    except Exception as e:
        messages.error(request, f"Erreur lors de la suppression de l'annonce : {str(e)}")
    return redirect('dashboard')

