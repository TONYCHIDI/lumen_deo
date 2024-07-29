# House forms.py
from django import forms
from .models import Houses, Project, Prototype


class HouseForm(forms.ModelForm):
    class Meta:
        model = Houses
        exclude = ["is_available"]

        labels = {
            'prototype': 'Prototype',
            'house_num': 'House Number',
            'subscri_price': 'Offered Price',
        }
        widgets = {
            'prototype': forms.Select(attrs={'class': 'form-control'}),
            'house_num': forms.TextInput(attrs={'class': 'form-control'}),
            'subscri_price': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        active_project = kwargs.pop('active_project', None)
        super().__init__(*args, **kwargs)
        
        if active_project:
            self.fields['prototype'].queryset = Prototype.objects.filter(project=active_project)
        else:
            self.fields['prototype'].queryset = Prototype.objects.none()



