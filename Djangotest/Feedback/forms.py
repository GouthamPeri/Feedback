from django import forms
from django.forms import formset_factory
from .models import *
from django.contrib.admin.widgets import AdminDateWidget


class LoginForm(forms.Form):
    id_no = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'placeholder': '14331A0560'}))
    #id_no.clean('14331A05D9')
    crypt_password = forms.CharField(widget=forms.PasswordInput)


class RegistrationForm(forms.Form):
    id_no = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'placeholder': '14331A0560'}))
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


def create_faculty_form(dept_code):

    class FacultyForm(forms.ModelForm):
        check = forms.CharField(widget=forms.CheckboxInput(attrs={'class': 'w3-check'}))
        joining_date = forms.DateTimeField(widget=forms.DateTimeInput)
        relieved_date = forms.DateTimeField(required=False)

        class Meta:
            model = Faculty
            fields = ['faculty_code', 'faculty_first_name', 'faculty_last_name', 'faculty_tel', 'faculty_email',
                      'home_department', 'joining_date', 'relieved_date']

        def __init__(self, *args, **kwargs):
            super(FacultyForm, self).__init__(*args, **kwargs)
            if dept_code:
                self.fields['home_department'].queryset = Department.objects.filter(
                    department_code=dept_code)
    return FacultyForm


class ProgramForm(forms.ModelForm):
    check = forms.CharField(widget=forms.CheckboxInput(attrs={'class': 'w3-check'}))
    class Meta:
        model=Program
        fields = ['program_code','program_name','inception_year','owner_department']


class RegulationForm(forms.ModelForm):
    check = forms.CharField(widget=forms.CheckboxInput(attrs={'class': 'w3-check'}))
    class Meta:
        model = Regulation
        fields = ['regulation_code', 'effective_from', 'total_required_credits']


def create_course_offered_form(dept_code):
    class CourseOfferedForm(forms.ModelForm):
        check = forms.CharField(widget=forms.CheckboxInput(attrs={'class': 'w3-check'}))
        class Meta:
            model = CourseOffered
            fields = ['course_code', 'regulation_code', 'program_code',
                      'subject_code', 'academic_year', 'semester', 'course_name', 'faculty_name']

        def __init__(self, *args, **kwargs):
            super(CourseOfferedForm, self).__init__(*args, **kwargs)
            if dept_code:
                self.fields['faculty_name'].queryset = Faculty.objects.filter(
                    home_department=dept_code)

    return CourseOfferedForm


class StudentTypeForm(forms.ModelForm):
    check = forms.CharField(widget=forms.CheckboxInput(attrs={'class': 'w3-check'}))
    class Meta:
        model = StudentType
        fields = ['student_type', 'student_type_desc']


class SubjectTypeForm(forms.ModelForm):
    check = forms.CharField(widget=forms.CheckboxInput(attrs={'class': 'w3-check'}))
    class Meta:
        model = SubjectType
        fields = ['subject_type', 'subject_type_desc']


class CourseRegistrationForm(forms.ModelForm):
    check = forms.CharField(widget=forms.CheckboxInput(attrs={'class': 'w3-check'}))

    class Meta:
        model = CourseOffered
        fields = ['course_code', 'regulation_code', 'program_code',
                  'subject_code', 'academic_year', 'semester', 'course_name', 'faculty_name']


class StudentForm(forms.ModelForm):
    check = forms.CharField(widget=forms.CheckboxInput(attrs={'class': 'w3-check'}))
    class Meta:
        model = Student
        fields = ['student_reg_no', 'student_first_name', 'student_last_name', 'student_type', 'academic_year_code', 'regulation_code']


class SubjectDeliveryTypeForm(forms.ModelForm):
    check = forms.CharField(widget=forms.CheckboxInput(attrs={'class': 'w3-check'}))
    class Meta:
        model = SubjectDeliveryType
        fields = ['subject_delivery_type', 'delivery_type_desc']


class SubjectOptionForm(forms.ModelForm):
    check = forms.CharField(widget=forms.CheckboxInput(attrs={'class': 'w3-check'}))
    class Meta:
        model = SubjectOption
        fields = ['regulation_code', 'program_code', 'subject_code', 'subject_option_code', 'subject_option_name', 'offered_by']


class ProgramStructureForm(forms.ModelForm):
    class Meta:
        model = ProgramStructure
        fields = ['regulation_code','program_code','semester','subject_code','subject_name','subject_type','subject_delivery_type',
                   'number_hpw','number_credits']
