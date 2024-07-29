from django import forms
from .models import Prototype

class PrototypeForm(forms.ModelForm):
    class Meta:
        model = Prototype
        fields = ['project', 'prototype_name', 'prototype_img', 'prototype_description', 'prototype_size', 'prototype_price', 'num_of_bedrooms', 'num_of_bathrooms', 'num_of_kitchen', 'num_of_parking_space', 'sewage_fee', 'water_fee']
        labels = {
            'prototype_name': 'Name of the Prototype',
            'prototype_img': 'Image of the Prototype',
            'prototype_description': 'Description of the Prototype',
            'prototype_size': 'Size of the Prototype',
            'prototype_price': 'Price of the Prototype',
            'num_of_bedrooms': 'Number of Bedrooms',
            'num_of_bathrooms': 'Number of Bathrooms',
            'num_of_kitchen': 'Number of Kitchens',
            'num_of_parking_space': 'Number of Parking Spaces',
            'sewage_fee': 'Sewage Fee',
            'water_fee': 'Water Fee',
        }
        widgets = {
            'project': forms.Select(attrs={'class': 'form-select'}),
            'prototype_name': forms.TextInput(attrs={'class': 'form-control'}),
            'prototype_img': forms.FileInput(attrs={'class': 'form-select'}),
            'prototype_description': forms.Textarea(attrs={'class': 'form-control', "rows": "2", "cols": "1"}),
            'prototype_size': forms.NumberInput(attrs={'class': 'form-control'}),
            'prototype_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'num_of_bedrooms': forms.NumberInput(attrs={'class': 'form-control'}),
            'num_of_bathrooms': forms.NumberInput(attrs={'class': 'form-control'}),
            'num_of_kitchen': forms.NumberInput(attrs={'class': 'form-control'}),
            'num_of_parking_space': forms.NumberInput(attrs={'class': 'form-control'}),
            'sewage_fee': forms.NumberInput(attrs={'class': 'form-control'}),
            'water_fee': forms.NumberInput(attrs={'class': 'form-control'}),
        }
