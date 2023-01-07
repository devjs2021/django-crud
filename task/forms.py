from django.forms import ModelForm
from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        
        fields = ['titulo', 'description', 'importante']
        widgets = {
            "titulo": forms.TextInput(attrs={'class': 'form-control'}),
            "description": forms.Textarea(attrs={'class': 'form-control'}),
            "importante": forms.CheckboxInput(attrs={'class': 'form-check-input text-center'})
            
        }