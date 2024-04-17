# -*- coding: utf-8 -*-

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Rapport, Medecin, Visiteur,Medicament
from django.core.exceptions import ValidationError
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

    def clean_login(self):
        login = self.cleaned_data.get('login')
        try:
            # Vérifie s'il existe déjà un visiteur avec le même login
            Visiteur.objects.get(login=login)
            raise ValidationError("Ce login est déjà utilisé. Veuillez en choisir un autre.")
        except Visiteur.DoesNotExist:
            # Si aucun visiteur avec ce login n'existe, alors le login est unique
            return login


class RapportForm(forms.ModelForm):
    quantite = forms.IntegerField(min_value=1)
    medicament = forms.ModelChoiceField(queryset=Medicament.objects.all(), empty_label=None)

    class Meta:
        model = Rapport
        fields = ['idvisiteur', 'daterapport', 'motif', 'bilan', 'idmedecin', 'medicament']
        widgets = {
            'daterapport': forms.DateInput(attrs={'type': 'date'}),
            'idmedecin': forms.Select(attrs={'class': 'form-select'})
        }



    def __init__(self, *args, **kwargs):
        super(RapportForm, self).__init__(*args, **kwargs)
        self.fields['idmedecin'].queryset = Medecin.objects.all()
        self.fields['idvisiteur'].widget.attrs['readonly'] = True  # Make the field read-only
        self.fields['idvisiteur'].disabled = True  # Disable the field

        # Define a list of tuples (ID of the doctor, name of the doctor) for the idmedecin field
        doctor_choices = [(doctor.idmedecin, f"{doctor.nom} {doctor.prenom}") for doctor in Medecin.objects.all()]
        self.fields['idmedecin'].choices = doctor_choices

        # Define a list of tuples (ID of the medication, name of the medication) for the medicament field
        medication_choices = [(medication.idmedicament, medication.nomcommercial) for medication in Medicament.objects.all()]
        self.fields['medicament'].choices = medication_choices



class VisiteurForm(forms.ModelForm):
    class Meta:
        model = Visiteur
        fields = ['nomvisiteur', 'prenomvisiteur', 'login', 'mdp', 'adressevisiteur', 'villevisiteur', 'cp_visiteur', 'dateembauchevisiteur']