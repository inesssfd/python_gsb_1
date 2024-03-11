# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import Visiteur, Medecin, Rapport

# Définir la classe MedecinAdmin
class MedecinAdmin(admin.ModelAdmin):
    list_display = ('idmedecin', 'nom', 'prenom', 'adresse', 'ville', 'cp_medecin', 'tel', 'specialistecomplementaire', 'departement')
class VisiteurAdmin(admin.ModelAdmin):
    list_display = ('idvisiteur', 'nomvisiteur', 'prenomvisiteur','login', 'mdp', 'adressevisiteur', 'villevisiteur', 'cp_visiteur', 'dateembauchevisiteur')
class RapportAdmin(admin.ModelAdmin):
    list_display = ('idrapport', 'daterapport', 'motif', 'idvisiteur_id', 'idmedecin_id')  # Champs à afficher dans la liste des objets Rapport
admin.site.register(Medecin, MedecinAdmin)

# Enregistrer les autres modèles
admin.site.register(Visiteur, VisiteurAdmin)
admin.site.register(Rapport, RapportAdmin)
