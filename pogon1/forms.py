from django import forms

from .models import Upravljanje

class UpravljanjeForm(forms.ModelForm):
    class Meta:
        model = Upravljanje
        fields = [
            'korisnik',
            'title',
            'content',
            'kod',
            'mcu',
            'model',
            'extra',
            'image',
        ]
