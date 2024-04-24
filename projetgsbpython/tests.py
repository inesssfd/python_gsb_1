from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Visiteur, Rapport, Medicament, MedicamentRapport
from .forms import RapportForm

class CreateRapportTestCase(TestCase):
    def setUp(self):
        # Créer un utilisateur pour simuler une connexion
        self.user = User.objects.create_user(username='test_user', password='password')

        # Créer un visiteur de test
        self.visiteur = Visiteur.objects.create(login='test', mdp='testmdp')

        # Créer un médicament de test
        self.medicament = Medicament.objects.create(nomcommercial='Test Medicament')
def test_create_rapport(self):
    self.client.login(username='test_user', password='password')

    # Obtenir l'URL de la vue create_rapport
    url = reverse('create_rapport', kwargs={'visiteur_id': self.visiteur.idvisiteur})

    # Récupérer tous les médecins de la base de données
    medecins = Medecin.objects.all()

    # Créer une liste d'options pour le champ idmedecin
    idmedecin_options = [(medecin.idmedecin, f"{medecin.nom} {medecin.prenom}") for medecin in medecins]

    # Données du formulaire à soumettre
    data = {
        'idvisiteur': self.visiteur.idvisiteur,
        'daterapport': '2024-04-25',  # Remplacer par la date appropriée
        'motif': 'Test Motif',        # Remplacer par le motif approprié
        'bilan': 'Test Bilan',        # Remplacer par le bilan approprié
        'idmedecin': idmedecin_options[0][0],  # Sélectionner le premier médecin de la liste
        'medicament': self.medicament.idmedicament,
        'quantite': 5,
    }

    # Soumettre le formulaire en tant que POST request
    response = self.client.post(url, data)

    # Imprimer les données de réponse pour le débogage
    print(response.content)

    # Vérifier si la redirection s'est faite avec succès
    self.assertEqual(response.status_code, 302)

    # Vérifier si le rapport a été créé avec succès
    self.assertTrue(Rapport.objects.filter(idvisiteur=self.visiteur).exists())

    # Vérifier si le médicament a été ajouté au rapport avec la quantité correcte
    rapport = Rapport.objects.get(idvisiteur=self.visiteur)
    medicament_rapport = MedicamentRapport.objects.get(idrapport=rapport, idmedicament=self.medicament)
    self.assertEqual(medicament_rapport.quantite, 5)
