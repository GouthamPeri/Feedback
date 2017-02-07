from django import forms
from django.forms import formset_factory
from .models import *


class LoginForm(forms.Form):
    id_no = forms.CharField(initial="14331A0500", max_length=10)
    id_no.clean('14331A05D9')
    crypt_password = forms.CharField(widget=forms.PasswordInput)


class RegistrationForm(forms.Form):
    id_no = forms.CharField(initial="Eg: 14331A0563", max_length=10)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)


class ChangePasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)


class FieldCountForm(forms.Form):
    add_empty_records = forms.IntegerField()


class DeleteForm(forms.Form):
    academic_year_code = forms.IntegerField()


class AcademicYearForm(forms.ModelForm):
    check = forms.CharField(widget=forms.CheckboxInput(attrs={'class':'w3-check'}))
    class Meta:
        model = AcademicYear
        fields = ['academic_year_code', 'academic_year']


class DepartmentForm(forms.ModelForm):
    check = forms.CharField(widget=forms.CheckboxInput(attrs={'class': 'w3-check'}))
    class Meta:
        model = Department
        fields = ['department_code', 'department_name', 'inception_year']


class FacultyForm(forms.ModelForm):
    check = forms.CharField(widget=forms.CheckboxInput(attrs={'class': 'w3-check'}))
    joining_date = forms.DateTimeField(widget=forms.DateTimeInput())
    relieved_date = forms.DateTimeField(widget=forms.DateTimeInput())
    class Meta:
        model = Faculty
        fields = ['faculty_code', 'faculty_first_name', 'faculty_last_name', 'faculty_tel', 'faculty_email',
                  'home_department', 'joining_date', 'relieved_date']



class testform(forms.Form):
    f = forms.SelectMultiple(choices=('hey', 'hi', 'none'))