# Subscription forms.py
from django import forms
from .models import Houses, Subscription

class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscription
        exclude = ["user", "date"]

        labels = {
            'house': 'Available Houses',
        }
        widgets = {
            'house': forms.Select(attrs={'class': 'form-control-file'}),
        }

    def __init__(self, *args, **kwargs):
        active_project = kwargs.pop('active_project', None)
        super().__init__(*args, **kwargs)
        
        if active_project:
            self.fields['house'].queryset = Houses.objects.filter(prototype__project=active_project, is_available=True)
        else:
            self.fields['house'].queryset = Houses.objects.none()
