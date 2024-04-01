# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import Visiteur, Medecin, Rapport, Medicament,MedicamentRapport

# Définir la classe MedecinAdmin
class MedecinAdmin(admin.ModelAdmin):
    list_display = ('idmedecin', 'nom', 'prenom', 'adresse', 'ville', 'cp_medecin', 'tel', 'specialistecomplementaire', 'departement')
class VisiteurAdmin(admin.ModelAdmin):
    list_display = ('idvisiteur', 'nomvisiteur', 'prenomvisiteur','login', 'mdp', 'adressevisiteur', 'villevisiteur', 'cp_visiteur', 'dateembauchevisiteur')
class RapportAdmin(admin.ModelAdmin):
    list_display = ('idrapport', 'daterapport', 'motif', 'idvisiteur_id', 'idmedecin_id')  # Champs à afficher dans la liste des objets Rapport
class MedicamentAdmin(admin.ModelAdmin):
    list_display = ('idmedicament', 'nomcommercial', 'famille_medicament', 'composition', 'effet', 'contreindication')  # Champs à afficher dans la liste des objets Rapport
class MedicamentRapportAdmin(admin.ModelAdmin):
    list_display = ('idmedicament', 'idrapport', 'quantite')  # Champs à afficher dans la liste des objets Rapport
class MedicamentRapportAdmin(admin.ModelAdmin):
    list_display = ('idmedicament_id', 'idrapport_id', 'quantite')  # Afficher les ID des médicaments et des rapports dans la liste des objets MedicamentRapport


admin.site.register(Medecin, MedecinAdmin)
admin.site.register(Visiteur, VisiteurAdmin)
admin.site.register(Rapport, RapportAdmin)
admin.site.register(Medicament,MedicamentAdmin)
admin.site.register(MedicamentRapport,MedicamentRapportAdmin)