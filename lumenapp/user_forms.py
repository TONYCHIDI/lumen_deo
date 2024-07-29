from django import forms
from .models import User
from django.contrib.auth.hashers import make_password

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',}), required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        
        labels = {
            'username': 'Username',
            'last_name': 'Last Name',
            'first_name': 'First Name',
            'email': 'Email Address',
            'password': 'Password',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        if self.cleaned_data['password']:
            user.password = make_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user