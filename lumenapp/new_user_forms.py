from django import forms
from .models import NewUser


GENDER = [
    ('Male', 'Male'),
    ('Female', 'Female'),
]


class NewUserForm(forms.ModelForm):
    class Meta:
        model = NewUser
        fields = ['user_name', 'first_name', 'last_name', 'middle_name', 'category', 'gender', 'phone_number', 'email_address', 'passport_photo']
        labels = {
            'user_name': 'Username',
            'last_name': 'Last Name',
            'first_name': 'First Name',
            'middle_name': 'Middle Name (Optional)',
            'category': 'User Category',
            'phone_number': 'Phone Number',
            'gender': 'Gender',
            'email_address': 'Email',
            'passport_photo': 'Passport Photo'
        }
        widgets = {
            'user_name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control',}),
            'category': forms.Select(attrs={'class': 'form-select', 'required': True}),
            'phone_number': forms.NumberInput(attrs={'class': 'form-control', 'required': True}),
            'gender': forms.Select(attrs={'class': 'form-select', 'required': True}, choices=GENDER),
            'email_address': forms.EmailInput(attrs={'class': 'form-control', 'required': True}),
            'passport_photo': forms.FileInput(attrs={'class': 'form-select',}),
        }