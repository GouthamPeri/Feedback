from django import forms
from django.forms import formset_factory
from .models import *
import datetime
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.admin.widgets import FilteredSelectMultiple


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
        #relieved_date = forms.DateTimeField(required=False)

        class Meta:
            model = Faculty
            fields = ['faculty_code', 'faculty_first_name', 'faculty_last_name', 'faculty_tel', 'faculty_email',
                      'home_department', 'joining_date', 'relieved_date']
            widgets = {
                'joining_date': forms.DateInput(attrs={'class': 'datepicker'}),
                'relieved_date': forms.DateInput(attrs={'class': 'datepicker','required' : "False"})
            }
        def __init__(self, *args, **kwargs):
            super(FacultyForm, self).__init__(*args, **kwargs)
            if dept_code:
                self.fields['home_department'].queryset = Department.objects.filter(
                    department_code=dept_code)

        def clean(self):
            cleaned_data = super(FacultyForm, self).clean()
            joining_date = cleaned_data.get("joining_date")
            relieved_date = cleaned_data.get("relieved_date")
            if relieved_date < joining_date:
                raise forms.ValidationError("WRONG DATES!")

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
            self.fields['regulation_code'].label_from_instance = lambda obj: str(obj.regulation_code)
            self.fields['program_code'].label_from_instance = lambda obj: str(obj.program_code)
            self.fields['subject_code'].label_from_instance = lambda obj: str(obj.subject_code)

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
    def __init__(self, *args, **kwargs):
        super(SubjectOptionForm, self).__init__(*args, **kwargs)
        self.fields['regulation_code'].label_from_instance = lambda obj: str(obj.regulation_code)
        self.fields['program_code'].label_from_instance = lambda obj: str(obj.program_code)
        self.fields['subject_code'].label_from_instance = lambda obj: str(obj.subject_code)


class ProgramStructureForm(forms.ModelForm):
    check = forms.CharField(widget=forms.CheckboxInput(attrs={'class': 'w3-check'}))
    class Meta:
        model = ProgramStructure
        fields = ['regulation_code','program_code','semester','subject_code','subject_name','subject_type','subject_delivery_type',
                   'number_hpw','number_credits']


class CourseFeedbackAssignmentForm(forms.ModelForm):
    check = forms.CharField(widget=forms.CheckboxInput(attrs={'class': 'w3-check'}))
    class Meta:
        model = CourseFeedbackAssignment
        fields = ['course_code', 'student_reg_no', 'cycle_no', 'start_date', 'end_date', 'feedback_weighting', 'is_given']


class CourseRegistrationForm(forms.ModelForm):
    check = forms.CharField(widget=forms.CheckboxInput(attrs={'class': 'w3-check'}))
    course_code = forms.ChoiceField()
    class Meta:
        model = Student
        fields = ['course_code','student_reg_no']


class FeedbackTypeForm(forms.ModelForm):
    check = forms.CharField(widget=forms.CheckboxInput(attrs={'class': 'w3-check'}))
    class Meta:
        model = FeedbackType
        fields = ['cycle_no','feedback_type_desc']
        widgets = {
            'feedback_type_desc': forms.Textarea()
        }

def create_course_selection_form(courses,selected_course=None):
    choices=[]
    for course in courses:
        choices.append((course.course_code,course.course_code))
    class CourseSelectionForm(forms.Form):
        course = forms.ChoiceField(choices=choices,
                                   widget=forms.Select(attrs={"onchange": "this.form.submit()",
                                                                "id": "selected_course", 'class': 'w3-select-30'}),
                                   initial=selected_course)

    return CourseSelectionForm


class FeedbackQuestionForm(forms.ModelForm):
    check = forms.CharField(widget=forms.CheckboxInput(attrs={'class': 'w3-check'}))
    class Meta:
        model = FeedbackQuestion
        fields = ['effective_from','cycle_no','question_no','question_text']
        widgets = {
            'effective_from': forms.DateInput(attrs={'class': 'datepicker'}),
            'question_text': forms.Textarea()
        }

    def clean(self):
        cleaned_data = super(FeedbackQuestionForm, self).clean()
        effective_from = cleaned_data.get("effective_from")
        present_date = datetime.datetime.now().date()
        if effective_from < present_date:
            raise forms.ValidationError("WRONG DATES!")


def create_student_question_form(questions, registered_courses):
    CHOICES = (
        ('5', 'Excellent'),
        ('4', 'Very Good'),
        ('3', 'Satisfactory'),
        ('2', 'Average'),
        ('1', 'Poor'),
    )
    class StudentQuestion(forms.Form):

        def __init__(self, *args, **kwargs):
            super(StudentQuestion,self).__init__(*args,**kwargs)
            for question in questions:
                key = str(question.question_no)
                self.fields[key]=forms.CharField(widget=forms.TextInput(attrs={'value' : str(question.question_text)}))
                for course in registered_courses:
                    self.fields[key + "_" + str(course.course_code.course_code)] = forms.CharField(widget=forms.TextInput(attrs={'value' : str(course.course_code.course_name)}))
                    self.fields[key + "_" + str(course.course_code.course_code) + "_rating"] = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    return StudentQuestion
