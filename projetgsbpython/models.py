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
    idrapport = models.BigAutoField(primary_key=True)
    daterapport = models.DateField()
    motif = models.CharField(max_length=50)
    bilan = models.TextField()
    idvisiteur = models.ForeignKey(Visiteur, on_delete=models.CASCADE, null=True, db_column='idvisiteur')
    idmedecin = models.ForeignKey(Medecin, on_delete=models.CASCADE, null=True, db_column='idmedecin')
    
    class Meta:
        db_table = 'rapport'
