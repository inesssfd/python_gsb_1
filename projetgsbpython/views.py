# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import InscriptionForm, RapportForm
from .models import Visiteur, Medecin, Rapport,Medicament,MedicamentRapport
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
def inscription(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            visiteur = form.save()  # Sauvegarde du visiteur nouvellement créé
            return redirect('tableau_de_bord', visiteur_id=visiteur.idvisiteur)  # Redirection avec l'ID du visiteur
    else:
        form = InscriptionForm()
    return render(request, 'inscription.html', {'form': form})
def connexion(request):
    if request.method == 'POST':
        login = request.POST.get('login')
        mdp = request.POST.get('mdp')
        try:
            visiteurs = Visiteur.objects.filter(login=login, mdp=mdp)
            if visiteurs.count() == 1:
                visiteur = visiteurs.first()
                messages.success(request, "Connexion réussie !")
                return redirect('tableau_de_bord', visiteur_id=visiteur.idvisiteur)
            elif visiteurs.count() == 0:
                messages.error(request, "Identifiants invalides. Veuillez réessayer.")
            else:
                messages.error(request, "Plusieurs utilisateurs avec les mêmes identifiants. Veuillez contacter l'administrateur.")
        except Visiteur.DoesNotExist:
            messages.error(request, "Identifiants invalides. Veuillez réessayer.")
    return render(request, 'connexion.html')

def tableau_de_bord(request, visiteur_id):
    try:
        visiteur = Visiteur.objects.get(idvisiteur=visiteur_id)
        # Récupérer tous les rapports associés à l'utilisateur actuel
        rapports = Rapport.objects.filter(idvisiteur=visiteur)
    except Visiteur.DoesNotExist:
        # Gérer le cas où l'ID du visiteur n'existe pas
        return render(request, '404.html')

    context = {
        'visiteur_id': visiteur_id,  # Passer l'ID du visiteur au contexte
        'rapports': rapports  # Passer les rapports associés au contexte
    }
    return render(request, 'tableau_de_bord.html', context)

# Dans views.py

# Dans views.py

def create_rapport(request, visiteur_id):
    if request.method == 'POST':
        form = RapportForm(request.POST, initial={'idvisiteur': visiteur_id})
        if form.is_valid():
            rapport = form.save(commit=False)
            rapport.idvisiteur_id = visiteur_id
            rapport.save()

            # Récupérer les données de la quantité et du médicament sélectionné
            quantite = form.cleaned_data['quantite']
            medicament = form.cleaned_data['medicament']

            # Créer un enregistrement dans la table de jointure MedicamentRapport
            MedicamentRapport.objects.create(idrapport=rapport, idmedicament=medicament, quantite=quantite)

            return redirect('tableau_de_bord', visiteur_id=visiteur_id)
    else:
        form = RapportForm(initial={'idvisiteur': visiteur_id})
    return render(request, 'create_rapport.html', {'visiteur_id': visiteur_id, 'form': form})


def modifier_rapport(request, rapport_id):
    rapport = get_object_or_404(Rapport, idrapport=rapport_id)
    
    if request.method == 'POST':
        form = RapportForm(request.POST, instance=rapport)
        
        if form.is_valid():
            # Récupérer l'ID du médecin à partir du formulaire
            id_medecin = request.POST.get('idmedecin')
            form.instance.idmedecin_id = id_medecin
            
            form.save()
            messages.success(request, "Rapport modifié avec succès.")
            return redirect('tableau_de_bord', visiteur_id=rapport.idvisiteur_id)
        else:
            print(form.errors)  # Afficher les erreurs pour le débogage
            messages.error(request, "Erreur lors de la modification du rapport. Veuillez réessayer.")
    else:
        form = RapportForm(instance=rapport)
    
    return render(request, 'modifier_rapport.html', {'rapport': rapport, 'form': form})


def supprimer_rapport(request, rapport_id):
    rapport = get_object_or_404(Rapport, idrapport=rapport_id)
    visiteur_id = rapport.idvisiteur_id
    rapport.delete()
    return HttpResponseRedirect(reverse('tableau_de_bord', args=(visiteur_id,)))


def index(request):
    return render(request, 'index.html')


def profil_visiteur(request, visiteur_id):
    visiteur = get_object_or_404(Visiteur, idvisiteur=visiteur_id)
    context = {
        'visiteur': visiteur,
    }
    return render(request, 'profil_visiteur.html', context)


