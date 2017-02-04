from django import forms
from .models import *

class LoginForm(forms.Form):
    id_no = forms.CharField()
    crypt_password = forms.CharField(widget=forms.TextInput(attrs={'type': 'password'}))