from django import forms
from .models import LoanInformation

class AddLoans(forms.ModelForm):
    
    class Meta:
        model = LoanInformation
        fields = [
            'loan_name',
            'principal',
            'interest_rate',
            'minimum_payment',
        ]
