# new_client_forms.py
from django import forms
from .models import NewUser


MEANS_OF_ID_CHOICES = [
    ('Select', 'Select'),
    ('Voter\'s Card', 'Voter\'s Card'),
    ('National Id Card', 'National ID Card'),
    ('International Passport', 'International Passport'),
    ('Driver\'s License', 'Driver\'s License'),
]


MARITAL_STATUS = [
    ('Select', 'Select'),
    ('Single', 'Single'),
    ('Married', 'Married'),
    ('Divorced', 'Divorced'),
    ('Complicated', 'Complicated'),
]



class NewStaffForm(forms.ModelForm):
    class Meta:
        model = NewUser
        fields = ['marital_status', 'dob', 'address', 'means_of_id', 'id_photo', 'employ_date', 'designation', 'salary', 'bank_name', 'acct_name', 'acct_number', 'next_of_kin', 'nok_address', 'nok_phone_number', 'nok_rlship']
        labels = {
            'marital_status': 'Marital Status',
            'dob': 'Date of Birth',
            'address': 'Staff Address',
            'means_of_id': 'Means of Identification',
            'id_photo': 'Id Card',
            'employ_date': 'Employment Date',
            'designation': 'Staff Designation',
            'salary': "Salary",
            'bank_name': 'Staff Bank',
            'acct_name': 'Name on the Bank Account',
            'acct_number': 'Account Number',
            'next_of_kin': 'Staff Next of Kin',
            'nok_address': 'Next of Kin Address',
            'nok_phone_number': 'Next of Kin Number',
            'nok_rlship': 'Relationship with the Next of Kin',
        }
        widgets = {
            'marital_status': forms.Select(attrs={'class': 'form-select', "required": True}, choices=MARITAL_STATUS),
            'dob': forms.DateInput(attrs={'class': 'form-control',  'type': 'date', "required": True}),
            'address': forms.TextInput(attrs={'class': 'form-control', "required": True}),
            'means_of_id': forms.Select(attrs={'class': 'form-select', "required": True}, choices=MEANS_OF_ID_CHOICES),   
            'id_photo': forms.FileInput(attrs={'class': 'form-select', "required": True}),   
            'designation': forms.TextInput(attrs={'class': 'form-control', "required": True}),
            'salary': forms.NumberInput(attrs={'class': 'form-control', "required": True}),
            'employ_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'bank_name': forms.TextInput(attrs={'class': 'form-control', "required": True}),
            'acct_name': forms.TextInput(attrs={'class': 'form-control', "required": True}),
            'acct_number': forms.NumberInput(attrs={'class': 'form-control', "required": True}),
            'next_of_kin': forms.TextInput(attrs={'class': 'form-control', "required": True}),
            'nok_address': forms.TextInput(attrs={'class': 'form-control', "required": True}),
            'nok_phone_number': forms.NumberInput(attrs={'class': 'form-control', "required": True}),
            'nok_rlship': forms.TextInput(attrs={'class': 'form-control', "required": True}),
        }