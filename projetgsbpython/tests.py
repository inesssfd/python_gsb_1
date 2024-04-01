from django.test import TestCase
from django.urls import reverse
from .models import Visiteur, Rapport, Medicament

class CreateRapportTestCase(TestCase):
    def setUp(self):
        self.visiteur = Visiteur.objects.create(login='test', mdp='testmdp')  # Création d'un visiteur de test
        self.medicament = Medicament.objects.create(nomcommercial='Test Medicament')  # Création d'un médicament de test

    def test_create_rapport(self):
        url = reverse('create_rapport', kwargs={'visiteur_id': self.visiteur.idvisiteur})
        data = {
            'idvisiteur': self.visiteur.idvisiteur,
            'quantite': 5,
            'medicament': self.medicament.idmedicament
        }
        response = self.client.post(url, data)
        
        # Vérifier si la redirection s'est faite avec succès
        self.assertEqual(response.status_code, 302)

        # Vérifier si le rapport a été créé avec succès
        self.assertTrue(Rapport.objects.filter(idvisiteur=self.visiteur).exists())

        # Vérifier si le rapport contient le médicament avec la quantité correcte
        rapport = Rapport.objects.get(idvisiteur=self.visiteur)
        medicament_rapport = rapport.medicaments_rapport.first()
        self.assertEqual(medicament_rapport.idmedicament, self.medicament)
        self.assertEqual(medicament_rapport.quantite, 5)
