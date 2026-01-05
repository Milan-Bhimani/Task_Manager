from django import forms
from .models import Person

# This is our PersonForm which is a ModelForm based on the Person model. This is Built in feature of Django to create forms based on models.
class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['name','age','team','skills']
        widgets = {
            'skills' : forms.CheckboxSelectMultiple(),  
        }
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 2 :
            raise forms.ValidationError("Name must be at least 2 characters long.")
        return name
    
