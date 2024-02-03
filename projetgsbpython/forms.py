from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Rapport, Medecin, Visiteur
class InscriptionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Envoyer'))

    class Meta:
        model = Visiteur
        fields = ['nomvisiteur', 'prenomvisiteur', 'login', 'mdp', 'adressevisiteur', 'villevisiteur', 'cp_visiteur', 'dateembauchevisiteur']
        widgets = {
            'dateembauchevisiteur': forms.DateInput(attrs={'type': 'date'}),
        }

        
class RapportForm(forms.ModelForm):
    class Meta:
        model = Rapport
        fields = ['idvisiteur', 'daterapport', 'motif', 'bilan', 'idmedecin']
        widgets = {
            'daterapport': forms.DateInput(attrs={'type': 'date'}),
            'idmedecin': forms.Select(attrs={'class': 'form-select'})
        }

    def __init__(self, *args, **kwargs):
        super(RapportForm, self).__init__(*args, **kwargs)
        self.fields['idmedecin'].queryset = Medecin.objects.all()
        self.fields['idvisiteur'].widget.attrs['readonly'] = True  # Rendre le champ en lecture seule
        self.fields['idvisiteur'].disabled = True  # Rendre le champ désactivé

        # Définir une liste de tuples (ID du médecin, nom du médecin) pour le champ idmedecin
        medecin_choices = [(medecin.idmedecin, f"{medecin.nom} {medecin.prenom}") for medecin in Medecin.objects.all()]
        self.fields['idmedecin'].choices = medecin_choices
