# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import InscriptionForm, RapportForm
from .models import Visiteur, Medecin, Rapport,Medicament,MedicamentRapport
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django import forms
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
    # Récupérer la valeur de l'ID du médecin sélectionné (si disponible)
    id_medecin = request.GET.get('id_medecin')
    
    # Si un médecin est sélectionné, récupérer tous les rapports associés à ce médecin
    if id_medecin:
        rapports = Rapport.objects.filter(idmedecin=id_medecin)
    else:
        # Si aucun médecin n'est sélectionné, récupérer tous les rapports associés à l'utilisateur actuel
        rapports = Rapport.objects.filter(idvisiteur=visiteur_id)
    
    context = {
        'visiteur_id': visiteur_id,  # Passer l'ID du visiteur au contexte
        'rapports': rapports,  # Passer les rapports associés au contexte
        'medecins': Medecin.objects.all()  # Passer tous les médecins pour la liste déroulante
    }
    return render(request, 'tableau_de_bord.html', context)

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
    medicament_rapports = rapport.medicamentrapport_set.all()
    all_medicaments = Medicament.objects.all()  # Récupérer tous les médicaments de la base de données
    
    if request.method == 'POST':
        form = RapportForm(request.POST, instance=rapport)  # Création du formulaire avec les données POST et l'instance du rapport existant

        if form.is_valid():
            id_medecin = request.POST.get('idmedecin')
            rapport.idmedecin_id = id_medecin
            form.save(commit=False)
            form.save()

            # Mettre à jour les quantités des médicaments associés à ce rapport
            for medicament_rapport in medicament_rapports:
                quantite = request.POST.get(f'quantite_{medicament_rapport.id}')
                medicament_rapport.quantite = quantite

                # Mettre à jour l'ID du médicament dans MedicamentRapport
                medicament_id = request.POST.get(f'medicament_{medicament_rapport.id}')  # Assurez-vous d'avoir un champ nommé medicament_ID pour chaque médicament_rapport
                medicament_rapport.idmedicament_id = medicament_id

                medicament_rapport.save()

            messages.success(request, "Rapport modifié avec succès.")
            return redirect('tableau_de_bord', visiteur_id=rapport.idvisiteur_id)
        else:
            print(form.errors)
            messages.error(request, "Erreur lors de la modification du rapport. Veuillez réessayer.")
    else:
        form = RapportForm(instance=rapport)  # Création du formulaire avec l'instance du rapport existant

    return render(request, 'modifier_rapport.html', {'rapport': rapport, 'form': form, 'medicament_rapports': medicament_rapports, 'all_medicaments': all_medicaments})

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


def modifier_profil_visiteur(request, visiteur_id):
    visiteur = get_object_or_404(Visiteur, idvisiteur=visiteur_id)

    if request.method == 'POST':
        # Récupérer les données du formulaire
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        login = request.POST.get('login')
        adresse = request.POST.get('adresse')
        ville = request.POST.get('ville')
        cp = request.POST.get('cp')
        date_embauche = request.POST.get('dateembauche')

        # Afficher les données récupérées pour le débogage
        print("Données du formulaire :")
        print("Nom :", nom)
        print("Prénom :", prenom)
        print("Login :", login)
        print("Adresse :", adresse)
        print("Ville :", ville)
        print("Code postal :", cp)
        print("Date d'embauche :", date_embauche)

        # Mettre à jour les données du visiteur
        visiteur.nomvisiteur = nom
        visiteur.prenomvisiteur = prenom
        visiteur.login = login
        visiteur.adressevisiteur = adresse
        visiteur.villevisiteur = ville
        visiteur.cp_visiteur = cp
        visiteur.dateembauchevisiteur = date_embauche
        visiteur.save()

        # Rediriger vers la page de profil avec un message de succès
        messages.success(request, "Profil mis à jour avec succès.")
        return redirect('profil_visiteur', visiteur_id=visiteur_id)

    # Si la méthode de la requête n'est pas POST, afficher le formulaire avec les données actuelles
    context = {
        'visiteur': visiteur,
    }
    return render(request, 'profil_visiteur.html', context)
