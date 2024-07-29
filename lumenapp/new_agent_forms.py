# new_client_forms.py
from django import forms
from .models import NewUser


MEANS_OF_ID_CHOICES = [
    ('Select', 'Select'),
    ("Voter's Card", "Voter's Card"),
    ('National Id Card', 'National ID Card'),
    ('International Passport', 'International Passport'),
    ("Driver's License", "Driver's License"),
]


MARITAL_STATUS = [
    ('Select', 'Select'),
    ('Single', 'Single'),
    ('Married', 'Married'),
    ('Divorced', 'Divorced'),
    ('Complicated', 'Complicated'),
]


class NewAgentForm(forms.ModelForm):
    class Meta:
        model = NewUser
        fields = ['marital_status', 'dob', 'occupation', 'address', 'agency_percentage', 'means_of_id', 'id_photo', 'next_of_kin', 'nok_address', 'nok_phone_number', 'nok_rlship', 'bank_name', 'acct_name', 'acct_number']
        labels = {
            'marital_status': 'Marital Status',
            'dob': 'Date of Birth',
            'occupation': 'Client Occupation',
            'address': 'Client Address',
            'agency_percentage': 'Agency',
            'means_of_id': 'Means of Identification',
            'id_photo': 'Id Card',
            'next_of_kin': 'Client Next of Kin',
            'nok_address': 'Next of Kin Address',
            'nok_phone_number': 'Next of Kin Number',
            'nok_rlship': 'Relationship with the Next of Kin',
            'bank_name': 'Name of Bank',
            'acct_name': 'Name on the Bank Account',
            'acct_number': 'Account Number',
        }
        widgets = {
            'marital_status': forms.Select(attrs={'class': 'form-select', "required": True}, choices=MARITAL_STATUS),
            'dob': forms.DateInput(attrs={'class': 'form-control',  'type': 'date', "required": True}),
            'occupation': forms.TextInput(attrs={'class': 'form-control', "required": True}),
            'address': forms.TextInput(attrs={'class': 'form-control', "required": True}),
            'agency_percentage': forms.NumberInput(attrs={'class': 'form-control', "required": True}),
            'means_of_id': forms.Select(attrs={'class': 'form-select', "required": True}, choices=MEANS_OF_ID_CHOICES),   
            'id_photo': forms.FileInput(attrs={'class': 'form-select', "required": True}),   
            'next_of_kin': forms.TextInput(attrs={'class': 'form-control', "required": True}),
            'nok_address': forms.TextInput(attrs={'class': 'form-control', "required": True}),
            'nok_phone_number': forms.NumberInput(attrs={'class': 'form-control', "required": True}),
            'nok_rlship': forms.TextInput(attrs={'class': 'form-control', "required": True}),
            'bank_name': forms.TextInput(attrs={'class': 'form-control', "required": True}),
            'acct_name': forms.TextInput(attrs={'class': 'form-control', "required": True,}),
            'acct_number': forms.NumberInput(attrs={'class': 'form-control', "required": True}),
        }