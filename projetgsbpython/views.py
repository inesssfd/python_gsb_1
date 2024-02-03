from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import InscriptionForm, RapportForm
from .models import Visiteur, Medecin, Rapport
from django.shortcuts import get_object_or_404

def inscription(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tableau_de_bord')
            return redirect('inscription')  # Rechargez la page pour afficher le formulaire vide
    else:
        form = InscriptionForm()  # Crée une instance du formulaire vide
    return render(request, 'inscription.html', {'form': form})

def connexion(request):
    if request.method == 'POST':
        login = request.POST.get('login')
        mdp = request.POST.get('mdp')
        try:
            visiteur = Visiteur.objects.get(login=login, mdp=mdp)
            messages.success(request, "Connexion réussie !")
            return redirect('tableau_de_bord', visiteur_id=visiteur.idvisiteur)  # Redirection avec l'ID du visiteur
        except Visiteur.DoesNotExist:
            messages.error(request, "Identifiants invalides. Veuillez réessayer.")
    return render(request, 'connexion.html')

def tableau_de_bord(request, visiteur_id):
    try:
        visiteur = Visiteur.objects.get(idvisiteur=visiteur_id)
    except Visiteur.DoesNotExist:
        # Gérer le cas où l'ID du visiteur n'existe pas
        return render(request, '404.html')

    context = {
        'visiteur_id': visiteur_id
    }
    return render(request, 'tableau_de_bord.html', context)

def create_rapport(request, visiteur_id):
    if request.method == 'POST':
        form = RapportForm(request.POST, initial={'idvisiteur': visiteur_id})  # Passer l'ID du visiteur au formulaire
        if form.is_valid():
            rapport = form.save(commit=False)
            rapport.idvisiteur_id = visiteur_id  # Assigner l'ID du visiteur connecté au rapport
            rapport.save()
            return redirect('tableau_de_bord', visiteur_id=visiteur_id)
    else:
        form = RapportForm(initial={'idvisiteur': visiteur_id})  # Passer l'ID du visiteur au formulaire
    return render(request, 'create_rapport.html', {'visiteur_id': visiteur_id, 'form': form})
