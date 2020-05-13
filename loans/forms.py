from django import forms
from .models import LoanInformation, Profile
from django.contrib.auth.models import User
from django.forms import ModelForm

class AddLoans(forms.ModelForm):

    class Meta:
        model = LoanInformation
        fields = [
            'loan_name',
            'principal',
            'interest_rate',
            'minimum_payment',
        ]

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = [
            'payoff_style',
            'extra_payment',
        ]

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name','username', 'email']
