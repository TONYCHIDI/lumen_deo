# new_client_forms.py
from django import forms
from .models import CompanyBank


class BankForm(forms.ModelForm):
    class Meta:
        model = CompanyBank
        fields = ("__all__")
        labels = {
            'com_bank': 'Bank Name',
            'acct_name': 'Company Account Name',
            'acct_num': 'Account Number',
        }
        widgets = {
            'com_bank': forms.TextInput(attrs={'class': 'form-control', "required": True}),
            'acct_name': forms.TextInput(attrs={'class': 'form-control', "required": True}),
            'acct_num': forms.NumberInput(attrs={'class': 'form-control', "required": True}),
        }