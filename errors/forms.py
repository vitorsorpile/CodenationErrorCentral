from django import forms
from errors.models import Error

class ErrorForm(forms.ModelForm):
    class Meta:
        model = Error
        fields = ['category', 'level', 'description']