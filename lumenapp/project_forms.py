# project_forms.py
from django import forms
from .models import Project


COMPLETED = [
    ('select', 'Select'),
    ('True', 'True'),
    ('False', 'False'),
]


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ["author"]  # Include all fields from the model  except the "author" field

        # Custom labels for fields
        labels = {
            'title': 'Project Title',
            'location': 'Location',
            'description': 'Description',
            'plot_no': 'Plot Number',
            'display_img': 'Display Image URL',
            'project_imgs': 'Project Images URL',
            'size': 'Size (in square meters)',
            'tot_num_of_bedrooms': 'Total Number of Bedrooms',
            'tot_num_of_bathrooms': 'Total Number of Bathrooms',
            'is_completed': 'Completed?',
            'plot_features': 'Plot Features',
            'title_doc_type': 'Title Document Type',
            'title_doc_num': 'Title Document Number',
            'title_doc_file_num': 'Title Document File Number',
            'title_doc_date': 'Title Document Date',
            'title_doc_vol': 'Title Document Volume',
            'title_doc_page': 'Title Document Page',
            'title_doc_reg_num': 'Title Document Registration Number',
            'landowner': 'Landowner',
            'landowner_address': 'Landowner\'s Address',
            'developers_share': 'Developer\'s Share',
        }

        # Custom widgets and other attributes
        widgets = {
            'author': forms.Select(attrs={'class': 'form-control', 'type': 'select'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 2, 'cols': 40, 'class': 'form-control'}),  # Textarea widget with specific rows and columns
            'plot_no': forms.TextInput(attrs={'class': 'form-control'}),
            'display_img': forms.FileInput(attrs={'class': 'form-select',}),
            'project_imgs': forms.FileInput(attrs={'class': 'form-select',}),
            'size': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),  # NumberInput with step attribute
            'is_completed': forms.Select(attrs={'class': 'form-select', 'required': True}, choices=COMPLETED),
            'plot_features': forms.TextInput(attrs={'class': 'form-control',}),
            'tot_num_of_bedrooms': forms.NumberInput(attrs={'class': 'form-control', 'min': '3'}),  # NumberInput with minimum value
            'tot_num_of_bathrooms': forms.NumberInput(attrs={'class': 'form-control', 'min': '3'}),
            'title_doc_type': forms.TextInput(attrs={'class': 'form-control',}),
            'title_doc_num': forms.TextInput(attrs={'class': 'form-control',}),
            'title_doc_file_num': forms.TextInput(attrs={'class': 'form-control',}),
            'title_doc_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),  # DateInput widget
            'title_doc_vol': forms.TextInput(attrs={'class': 'form-control',}),
            'title_doc_page': forms.TextInput(attrs={'class': 'form-control',}),
            'title_doc_reg_num': forms.TextInput(attrs={'class': 'form-control',}),
            'landowner': forms.TextInput(attrs={'class': 'form-control',}),
            'landowner_address': forms.TextInput(attrs={'class': 'form-control',}),
            'developers_share': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
        # Custom help texts
        help_texts = {
            'title_doc_num': '[C of O] or [R of O] Number',
            'title_doc_date': 'Enter the date of the title document.',
            'landowner': 'Name of the landowner or joint venture partner.',
            'landowner_address': 'Address of the landowner or joint venture partner.',
            'developers_share': 'Percentage or share of the developer in the project.',
        }

      