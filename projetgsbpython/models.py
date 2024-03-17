# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
class Visiteur(models.Model):
    idvisiteur  = models.BigAutoField(primary_key=True)  # Utilisation de BigAutoField pour une clé primaire auto-incrémentée
    nomvisiteur = models.CharField(max_length=50, null=True, blank=True)
    prenomvisiteur  = models.CharField(max_length=50, null=True, blank=True)
    login = models.CharField(max_length=50, null=True, blank=True)
    mdp = models.CharField(max_length=50, null=True, blank=True)
    adressevisiteur = models.CharField(max_length=50, null=True, blank=True)
    villevisiteur = models.CharField(max_length=50, null=True, blank=True)
    cp_visiteur = models.IntegerField(null=True, blank=True)
    dateembauchevisiteur = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'visiteur'  # Nom de la table dans la base de données



class Medecin(models.Model):
    idmedecin   = models.BigAutoField(primary_key=True)  # Utilisation de BigAutoField pour une clé primaire auto-incrémentée
    nom = models.CharField(max_length=50, null=True, blank=True)
    prenom = models.CharField(max_length=50, null=True, blank=True)
    adresse = models.CharField(max_length=50, null=True, blank=True)
    ville = models.CharField(max_length=50, null=True, blank=True)
    cp_medecin = models.CharField(max_length=50, null=True, blank=True)
    tel = models.CharField(max_length=50, null=True, blank=True)
    specialistecomplementaire  = models.CharField(max_length=50, null=True, blank=True)
    departement = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = 'medecin'  # Nom de la table dans la base de données



class Rapport(models.Model):
    idrapport = models.AutoField(primary_key=True)
    daterapport = models.DateField()
    motif = models.CharField(max_length=50)
    bilan = models.TextField()
    idvisiteur = models.ForeignKey(Visiteur, on_delete=models.CASCADE, null=True, db_column='idvisiteur')
    idmedecin = models.ForeignKey(Medecin, on_delete=models.CASCADE, null=True, db_column='idmedecin')

    class Meta:
        db_table = 'rapport'

class Medicament(models.Model):
    idmedicament = models.AutoField(primary_key=True)
    nomcommercial = models.CharField(max_length=100)
    famille_medicament = models.CharField(max_length=100)
    composition = models.TextField()
    effet = models.TextField()
    contreindication = models.TextField()

    class Meta:
        db_table = 'medicament'

class MedicamentRapport(models.Model):
    idmedicament = models.ForeignKey(Medicament, on_delete=models.CASCADE, db_column='idmedicament')  # Assurez-vous que le nom de la colonne correspond à celui dans la table Medicament
    idrapport = models.ForeignKey(Rapport, on_delete=models.CASCADE, db_column='idrapport')  # Assurez-vous que le nom de la colonne correspond à celui dans la table Rapport
    quantite = models.IntegerField()

    class Meta:
        db_table = 'medicament_rapport'  # Nom de la table dans la base de données

    def __str__(self):
        return f"Medicament {self.idmedicament} dans le rapport {self.idrapport} - Quantité: {self.quantite}"
