# user_category_forms.py
from django import forms
from .models import UserCategory

class UserCategoryForm(forms.ModelForm):
    class Meta:
        model = UserCategory
        fields = ['user_category']
        
        labels = {
            'user_category': 'User Category',
        }
        widgets = {
            'user_category': forms.TextInput(attrs={'class': 'form-control'}),
        }