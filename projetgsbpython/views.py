from django.core.exceptions import ObjectDoesNotExist
# Import pour utiliser la fonctionnalité de messagerie de Django
from django.contrib import messages
# Imports liés à la gestion des vues dans Django
from django.shortcuts import render, get_object_or_404, redirect
# Imports des formulaires définis dans l'application
from .forms import InscriptionForm, RapportForm, VisiteurForm
# Imports des modèles définis dans l'application
from .models import Visiteur, Medecin, Rapport, Medicament, MedicamentRapport
# Import de la fonction reverse pour générer des URLs à partir des noms des vues
from django.urls import reverse
from django import forms# Import de la classe Form de Django pour accéder aux éléments liés aux formulaires
# Import de la fonction logout de Django pour déconnecter l'utilisateur actuellement authentifié
from django.contrib.auth import logout
# Import de la classe Q de Django pour créer des requêtes complexes
from django.db.models import Q
# Import pour gérer les réponses HTTP et les erreurs 403
from django.http import HttpResponseRedirect, HttpResponseForbidden


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

            return redirect('tableau_de_bord', visiteur_id=visiteur_id)  # Redirection vers le tableau de bord
    else:
        form = RapportForm(initial={'idvisiteur': visiteur_id})
    return render(request, 'create_rapport.html', {'visiteur_id': visiteur_id, 'form': form})


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


def supprimer_visiteur(request, visiteur_id):
    # Récupérer le visiteur à supprimer
    visiteur = get_object_or_404(Visiteur, idvisiteur=visiteur_id)
    
    if request.method == 'POST':
        # Supprimer le visiteur
        visiteur.delete()
        
        # Ajouter un message de succès
        messages.success(request, "Le visiteur a été supprimé avec succès.")
        
        # Rediriger vers une page appropriée (par exemple, la page d'accueil)
        return redirect('index')
    
    # Si la méthode de la requête n'est pas POST, afficher un message d'erreur
    messages.error(request, "La suppression du visiteur a échoué. Veuillez réessayer.")
    return redirect('profil_visiteur', visiteur_id=visiteur_id)  # Rediriger vers le profil du visiteur



def modifier_visiteur(request, visiteur_id):
    visiteur = get_object_or_404(Visiteur, idvisiteur=visiteur_id)
    
    
    if request.method == 'POST':
        form = VisiteurForm(request.POST, instance=visiteur)
        if form.is_valid():
            form.save()
            messages.success(request, "Les informations du visiteur ont été mises à jour avec succès.")
            return redirect('profil_visiteur', visiteur_id=visiteur_id)
    else:
        form = VisiteurForm(instance=visiteur)
    return render(request, 'modifier_visiteur.html', {'form': form})

def modifier_rapport(request, rapport_id):
    rapport = get_object_or_404(Rapport, idrapport=rapport_id)

    
    if request.method == 'POST':
        form = RapportForm(request.POST, instance=rapport)
        if form.is_valid():
            form.save()

            # Récupérer les données de la quantité et du médicament sélectionné
            quantite = form.cleaned_data['quantite']
            medicament = form.cleaned_data['medicament']

            # Mettre à jour l'entrée dans la table MedicamentRapport associée à ce rapport
            medicament_rapport = rapport.medicamentrapport_set.first()
            if medicament_rapport:
                medicament_rapport.quantite = quantite
                medicament_rapport.idmedicament = medicament
                medicament_rapport.save()
            else:
                # Si aucune entrée n'existe dans la table MedicamentRapport, créer une nouvelle entrée
                MedicamentRapport.objects.create(idrapport=rapport, idmedicament=medicament, quantite=quantite)

            messages.success(request, "Le rapport a été modifié avec succès.")
            return redirect('tableau_de_bord', visiteur_id=rapport.idvisiteur_id)
    else:
        initial_data = {
            'medicament': rapport.medicamentrapport_set.first().idmedicament if rapport.medicamentrapport_set.exists() else None,
            'quantite': rapport.medicamentrapport_set.first().quantite if rapport.medicamentrapport_set.exists() else None
        }
        form = RapportForm(instance=rapport, initial=initial_data)
    return render(request, 'modifier_rapport.html', {'form': form})

def liste_medecins(request):
    idmedecin = request.GET.get('idmedecin')
    if idmedecin:
        medecin = get_object_or_404(Medecin, idmedecin=idmedecin)
        medecins = [medecin]
    else:
        medecins = Medecin.objects.all()
    return render(request, 'liste_medecins.html', {'medecins': medecins})


def deconnexion(request):
    logout(request)
    return redirect('index')