from django import forms
from models import Reporter1

class ReporterForm(forms.ModelForm):
    class Meta:
        model=Reporter1
        fields = ['name','age']