from django.http import HttpResponse
#from .models import *
from django.urls import reverse
from django.urls import reverse_lazy

from .forms import *
from django.forms import modelformset_factory, formset_factory
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views import View
from django.db.models import ProtectedError
from django.utils.functional import curry
from functools import partial, wraps
from django.db.models import Count



def is_dept_admin(user):
    return user.groups.filter(name="Dept Admin").exists();


def is_colg_admin(user):
    return user.groups.filter(name="Colg Admin").exists();


def is_student(user):
    return user.groups.filter(name="Student").exists();


def is_faculty(user):
    return user.groups.filter(name="Faculty").exists();


def login_view(request):
    error=''
    if request.method == 'POST':
        if 'crypt_password' in request.POST:
            form = LoginForm(request.POST)
            username = request.POST['id_no']
            password = request.POST['crypt_password']
            user = authenticate(username=username, password=password)
            if not user is None:
                login(request, user)
                if is_dept_admin(user):
                    return HttpResponseRedirect('/feedback/dept_admin')
                elif is_colg_admin(user):
                    return HttpResponseRedirect('/feedback/admin')
                elif is_student(user):
                    return HttpResponseRedirect('/feedback/view_courses')
                elif is_faculty(user):
                    return HttpResponseRedirect('/feedback/faculty_home_page')
            else:
                error = "Invalid Authentication"
        '''else:
            form2 = RegistrationForm(request)
            username = request.POST['id_no']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            if password1 != password2:
                return HttpResponse("Passwords Mismatch")
            if len(username) != 10:
                return HttpResponse("Invalid Username")
            User.objects.create_user(username.upper(),'example@gmail.com',password1).save()
            return HttpResponse("<h1>Successfully Registered</h1>")'''
    else:
        form = LoginForm()
    return render_to_response("login.html", {'form': form, 'error': error})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


@login_required
def index(request):
    return HttpResponse("hello " + request.user.username)


@login_required
@user_passes_test(is_colg_admin)
def admin_header(request):
    return render_to_response("admin_header.html", {'username': request.user.username})


@login_required
@user_passes_test(is_dept_admin)
def dept_admin_header(request):
    return render_to_response("dept_admin_header.html", {'username': request.user.username})


@login_required
@user_passes_test(is_student)
def student_header(request):
    return render_to_response("student_header.html", {'username': request.user.username})

@login_required
@user_passes_test(is_colg_admin)
def academic_year(request):
    error = ''
    entries = 1
    myformset = modelformset_factory(AcademicYear, AcademicYearForm, extra=entries)
    formset=myformset(queryset=AcademicYear.objects.none())
    countform = FieldCountForm()
    deleteform = DeleteForm()
    if request.method == 'POST':
        if 'add_empty_records' in request.POST: #add rows
            entries = int(request.POST['add_empty_records'])
            myformset = modelformset_factory(AcademicYear, AcademicYearForm, extra=entries)
            formset = myformset(queryset=AcademicYear.objects.none())
        elif 'form-0-academic_year_code' in request.POST: #add records
            formset = myformset(request.POST, queryset=AcademicYear.objects.none())
            if formset.is_valid():
                formset.save()
                formset = myformset(queryset=AcademicYear.objects.none())
            else:
                error = "ERROR: Already exists/Invalid/Empty records"
        else: #delete selected records
            indices = ''.join(request.POST.keys()).replace("form-", '').replace("-check", ' ').split()
            indices = list(map(int, indices))
            indices.sort(reverse=True)
            objects = AcademicYear.objects.all()
            try:
                for i in indices:
                    objects[i].delete()
            except ProtectedError as p:
                error = str(p)
                error = error[error.find('"')+1: error.find('"', 4)]
            except:
                error = "ERROR: Year code does not exist/Error performing deletion"

    else:
        formset = myformset(queryset=AcademicYear.objects.none())
        countform = FieldCountForm()
        deleteform = DeleteForm()

    return render_to_response('academic_year.html', {'formset': formset, 'countform': countform, 'deleteform': deleteform,
                                                    'database': myformset(), 'username': request.user.username,
                                                    'error': error})


@login_required
@user_passes_test(is_dept_admin)
def faculty(request):
    current_faculty = Faculty.objects.get(faculty_code=request.user.username)
    dept = current_faculty.home_department
    FacultyForm = create_faculty_form(dept)
    error = ''
    entries = 1
    myformset = modelformset_factory(Faculty, FacultyForm, extra=entries)
    formset=myformset(queryset=Faculty.objects.none())
    countform = FieldCountForm()
    deleteform = DeleteForm()
    if request.method == 'POST':
        if 'add_empty_records' in request.POST: # add rows
            entries = int(request.POST['add_empty_records'])
            myformset = modelformset_factory(Faculty, FacultyForm, extra=entries)
            formset = myformset(queryset=Faculty.objects.none())
        elif 'form-0-faculty_code' in request.POST: # add records
            formset = myformset(request.POST, queryset=Faculty.objects.none())
            if formset.is_valid():
                formset.save()
                formset = myformset(queryset=Faculty.objects.none())
            else:
                error = "ERROR: Already exists/Empty records/Invalid Data or Dates"
        else: # delete selected records
            print request.POST
            indices = ''.join(request.POST.keys()).replace("form-", '').replace("-check", ' ').split()
            indices = list(map(int, indices))
            indices.sort(reverse=True)
            objects = Faculty.objects.filter(home_department=dept)
            print objects
            print indices
            try:
                for i in indices:
                    faculty = objects[i]
                    print faculty
                    print faculty.faculty_code
                    if faculty.faculty_code == current_faculty.faculty_code:
                        error = "ERROR: You cannot delete your own record"
                    else:
                        print "h"
                        faculty.delete()
                        print "h"
            except ProtectedError as e:
                error = e
            except:
                error = "ERROR: Faculty code does not exist/Error performing deletion"

    else:
        myformset = modelformset_factory(Faculty, form=FacultyForm, extra=entries)
        formset = myformset(queryset=Faculty.objects.none())
        countform = FieldCountForm()
        deleteform = DeleteForm()

    dept = Faculty.objects.get(faculty_code=request.user.username).home_department
    queryset = Faculty.objects.filter(home_department = dept)
    return render_to_response('faculty.html', {'formset': formset, 'countform': countform, 'deleteform': deleteform,
                                                    'database': myformset(queryset=queryset), 'username': request.user.username,
                                                    'error': error})


@login_required
def change_password(request):
    header = ''
    if is_colg_admin(request.user):
        header = reverse('admin')
    elif is_dept_admin(request.user):
        header = reverse('dept_admin')
    elif is_student(request.user) or is_faculty(request.user):
        header = reverse('student_header')
    error = ''
    password_form = ChangePasswordForm()
    if request.method == 'POST':
        if not authenticate(username=request.user.username, password=request.POST['password']) is None:
            try:
                user = User.objects.get(username=request.user.username)
                if request.POST['password1'] == request.POST['password2']:
                    user.set_password(request.POST['password1'])
                    user.save()
                    logout(request)
                    return HttpResponseRedirect(reverse('login'))
                else:
                    error="Passwords mismatch!"
            except:
                error = "Error changing password"
        else:
            error = "Wrong password!"
    else:
        password_form = ChangePasswordForm()

    return render_to_response('change_password.html', {'password_form':password_form, 'error': error,
                                                       'username':request.user.username, 'header': header})


@login_required
@user_passes_test(is_colg_admin)
def regulation(request):
    error = ''
    entries = 1
    myformset = modelformset_factory(Regulation, RegulationForm, extra=entries)
    formset=myformset(queryset=Regulation.objects.none())
    countform = FieldCountForm()
    deleteform = DeleteForm()
    if request.method == 'POST':
        if 'add_empty_records' in request.POST: #add rows
            entries = int(request.POST['add_empty_records'])
            myformset = modelformset_factory(Regulation, RegulationForm, extra=entries)
            formset = myformset(queryset=Regulation.objects.none())
        elif 'form-0-regulation_code' in request.POST: #add records
            formset = myformset(request.POST, queryset=Regulation.objects.none())
            if formset.is_valid():
                formset.save()
                formset = myformset(queryset=Regulation.objects.none())
            else:
                error = "ERROR: Already exists / Invalid / Empty records"
        else: #delete selected records
            indices = ''.join(request.POST.keys()).replace("form-", '').replace("-check", ' ').split()
            indices = list(map(int, indices))
            indices.sort(reverse=True)
            objects = Regulation.objects.all()
            try:
                for i in indices:
                    objects[i].delete()
            except:
                error = "ERROR:Regulation code does not exist / Error performing deletion"
    else:
        formset = myformset(queryset=Regulation.objects.none())
        countform = FieldCountForm()
        deleteform = DeleteForm()
    return render_to_response('regulation.html', {'formset': formset, 'countform': countform, 'deleteform': deleteform,
                                               'database': myformset(), 'username': request.user.username,
                                               'error': error})


@login_required
@user_passes_test(is_colg_admin)
def department(request):
    error = ''
    entries = 1
    myformset = modelformset_factory(Department, DepartmentForm, extra=entries)
    formset=myformset(queryset=Department.objects.none())
    countform = FieldCountForm()
    deleteform = DeleteForm()
    if request.method == 'POST':
        if 'add_empty_records' in request.POST: #add rows
            entries = int(request.POST['add_empty_records'])
            myformset = modelformset_factory(Department, DepartmentForm, extra=entries)
            formset = myformset(queryset=Department.objects.none())
        elif 'form-0-department_code' in request.POST: #add records
            formset = myformset(request.POST, queryset=Department.objects.none())
            if formset.is_valid():
                formset.save()
                formset = myformset(queryset=Department.objects.none())
            else:
                error = "ERROR: Already exists/Invalid/Empty records"
        else: #delete selected records
            indices = ''.join(request.POST.keys()).replace("form-", '').replace("-check", ' ').split()
            indices = list(map(int, indices))
            indices.sort(reverse=True)
            objects = Department.objects.all()
            try:
                for i in indices:
                    objects[i].delete()
            except ProtectedError as p:
                error = str(p)
                error = error[error.find('"') + 1: error.find('"', 4)]
            except:
                error = "ERROR: Year code does not exist/Error performing deletion"
    else:
        formset = myformset(queryset=Department.objects.none())
        countform = FieldCountForm()
        deleteform = DeleteForm()
    return render_to_response('department.html', {'formset': formset, 'countform': countform, 'deleteform': deleteform,
                                               'database': myformset(), 'username': request.user.username,
                                               'error': error})

@login_required
@user_passes_test(is_colg_admin)
def add_program(request):
    error = ''
    entries = 1
    myformset = modelformset_factory(Program, ProgramForm, extra=entries)
    formset = myformset(queryset=Program.objects.none())
    countform = FieldCountForm()
    deleteform = DeleteForm()
    if request.method == 'POST':
        if 'add_empty_records' in request.POST:  # add rows
            entries = int(request.POST['add_empty_records'])
            myformset = modelformset_factory(Program, ProgramForm, extra=entries)
            formset = myformset(queryset=Program.objects.none())
        elif 'form-0-program_code' in request.POST:  # add records
            formset = myformset(request.POST, queryset=Program.objects.none())
            if formset.is_valid():
                formset.save()
                formset = myformset(queryset=Program.objects.none())
            else:
                error = "ERROR: Already exists / Invalid / Empty records"
        else:  # delete selected records
            indices = ''.join(request.POST.keys()).replace("form-", '').replace("-check", ' ').split()
            indices = list(map(int, indices))
            indices.sort(reverse=True)
            objects = Program.objects.all()
            try:
                for i in indices:
                    objects[i].delete()
            except:
                error = "ERROR:Program code does not exist / Error performing deletion"
    else:
        formset = myformset(queryset=Program.objects.none())
        countform = FieldCountForm()
        deleteform = DeleteForm()
    return render_to_response('program.html', {'formset': formset, 'countform': countform, 'deleteform': deleteform,
                                                  'database': myformset(), 'username': request.user.username,
                                                  'error': error})


@login_required
@user_passes_test(is_dept_admin)
def course_offered(request):
    dept = Faculty.objects.get(faculty_code=request.user.username).home_department
    CourseOfferedForm = create_course_offered_form(dept)
    error = ''
    entries = 1
    myformset = modelformset_factory(CourseOffered, CourseOfferedForm, extra=entries)
    formset = myformset(queryset=CourseOffered.objects.none())
    countform = FieldCountForm()
    deleteform = DeleteForm()
    if request.method == 'POST':
        if 'add_empty_records' in request.POST:  # add rows
            entries = int(request.POST['add_empty_records'])
            myformset = modelformset_factory(CourseOffered, CourseOfferedForm, extra=entries)
            formset = myformset(queryset=CourseOffered.objects.none())
        elif 'form-0-course_code' in request.POST:  # add records
            formset = myformset(request.POST, queryset=CourseOffered.objects.none())
            if formset.is_valid():
                formset.save()
                formset = myformset(queryset=CourseOffered.objects.none())
            else:
                error = "ERROR: Already exists/Invalid/Empty records"
        else:  # delete selected records
            indices = ''.join(request.POST.keys()).replace("form-", '').replace("-check", ' ').split()
            indices = list(map(int, indices))
            indices.sort(reverse=True)
            objects = CourseOffered.objects.all()
            try:
                for i in indices:
                    objects[i].delete()
            except ProtectedError as p:
                error = str(p)
                error = error[error.find('"') + 1: error.find('"', 4)]
            except:
                error = "ERROR: Course code does not exist/Error performing deletion"

    else:
        print myformset()
        formset = myformset(queryset=CourseOffered.objects.none())
        countform = FieldCountForm()
        deleteform = DeleteForm()

    return render_to_response('course_offered.html',
                              {'formset': formset, 'countform': countform, 'deleteform': deleteform,
                               'database': myformset(), 'username': request.user.username,
                               'error': error})


@login_required
@user_passes_test(is_dept_admin)
def course_reg(request):
    dept = Faculty.objects.get(faculty_code=request.user.username).home_department
    error = ''
    entries = 1
    myformset = modelformset_factory(AcademicYear, AcademicYearForm, extra=entries)
    formset = myformset(queryset=AcademicYear.objects.none())
    countform = FieldCountForm()
    deleteform = DeleteForm()
    if request.method == 'POST':
        if 'add_empty_records' in request.POST:  # add rows
            entries = int(request.POST['add_empty_records'])

            myformset = modelformset_factory(AcademicYear, AcademicYearForm, extra=entries)
            formset = myformset(queryset=AcademicYear.objects.none())
        elif 'form-0-academic_year_code' in request.POST:  # add records
            formset = myformset(request.POST, queryset=AcademicYear.objects.none())
            if formset.is_valid():
                formset.save()
                formset = myformset(queryset=AcademicYear.objects.none())
            else:
                error = "ERROR: Already exists/Invalid/Empty records"
        else:  # delete selected records
            indices = ''.join(request.POST.keys()).replace("form-", '').replace("-check", ' ').split()
            indices = list(map(int, indices))
            indices.sort(reverse=True)
            objects = AcademicYear.objects.all()
            try:
                for i in indices:
                    objects[i].delete()
            except ProtectedError as p:
                error = str(p)
                error = error[error.find('"') + 1: error.find('"', 4)]
            except:
                error = "ERROR: Year code does not exist/Error performing deletion"

    else:
        formset = myformset(queryset=AcademicYear.objects.none())
        countform = FieldCountForm()
        deleteform = DeleteForm()



    return render_to_response('course_registration.html',
                              {'formset': formset, 'countform': countform, 'deleteform': deleteform,
                               'database': myformset(), 'username': request.user.username,
                               'error': error})


@login_required
@user_passes_test(is_dept_admin)
def course_feedback_assgn(request):
    error = ''
    entries = 1
    myformset = modelformset_factory(AcademicYear, AcademicYearForm, extra=entries)
    formset = myformset(queryset=AcademicYear.objects.none())
    countform = FieldCountForm()
    deleteform = DeleteForm()
    if request.method == 'POST':
        if 'add_empty_records' in request.POST:  # add rows
            entries = int(request.POST['add_empty_records'])

            myformset = modelformset_factory(AcademicYear, AcademicYearForm, extra=entries)
            formset = myformset(queryset=AcademicYear.objects.none())
        elif 'form-0-academic_year_code' in request.POST:  # add records
            formset = myformset(request.POST, queryset=AcademicYear.objects.none())
            if formset.is_valid():
                formset.save()
                formset = myformset(queryset=AcademicYear.objects.none())
            else:
                error = "ERROR: Already exists/Invalid/Empty records"
        else:  # delete selected records
            indices = ''.join(request.POST.keys()).replace("form-", '').replace("-check", ' ').split()
            indices = list(map(int, indices))
            indices.sort(reverse=True)
            objects = AcademicYear.objects.all()
            try:
                for i in indices:
                    objects[i].delete()
            except ProtectedError as p:
                error = str(p)
                error = error[error.find('"') + 1: error.find('"', 4)]
            except:
                error = "ERROR: Year code does not exist/Error performing deletion"

    else:
        formset = myformset(queryset=AcademicYear.objects.none())
        countform = FieldCountForm()
        deleteform = DeleteForm()

    return render_to_response('academic_year.html',
                              {'formset': formset, 'countform': countform, 'deleteform': deleteform,
                               'database': myformset(), 'username': request.user.username,
                               'error': error})


@login_required
@user_passes_test(is_dept_admin)
def student(request):
    error = ''
    entries = 1
    myformset = modelformset_factory(Student, StudentForm, extra=entries)
    formset = myformset(queryset=Student.objects.none())
    countform = FieldCountForm()
    deleteform = DeleteForm()
    if request.method == 'POST':
        if 'add_empty_records' in request.POST:  # add rows
            entries = int(request.POST['add_empty_records'])

            myformset = modelformset_factory(Student, StudentForm, extra=entries)
            formset = myformset(queryset=Student.objects.none())
        elif 'form-0-student_reg_no' in request.POST:  # add records
            formset = myformset(request.POST, queryset=Student.objects.none())
            if formset.is_valid():
                formset.save()
                formset = myformset(queryset=Student.objects.none())
            else:
                error = "ERROR: Already exists/Invalid/Empty records"
        else:  # delete selected records
            indices = ''.join(request.POST.keys()).replace("form-", '').replace("-check", ' ').split()
            indices = map(int, indices)
            indices.sort(reverse=True)
            objects = Student.objects.all()
            try:
                for i in indices:
                    objects[i].delete()
            except ProtectedError as p:
                error = str(p)
                error = error[error.find('"') + 1: error.find('"', 4)]
            except:
                error = "ERROR: Student Reg code does not exist/Error performing deletion"

    else:
        countform = FieldCountForm()
        deleteform = DeleteForm()

    return render_to_response('student.html',
                              {'formset': formset, 'countform': countform, 'deleteform': deleteform,
                               'database': myformset(), 'username': request.user.username,
                               'error': error})


@login_required
@user_passes_test(is_dept_admin)
def student_type(request):
    error = ''
    entries = 1
    myformset = modelformset_factory(StudentType, StudentTypeForm, extra=entries)
    formset = myformset(queryset=StudentType.objects.none())
    countform = FieldCountForm()
    deleteform = DeleteForm()
    if request.method == 'POST':
        if 'add_empty_records' in request.POST:  # add rows
            entries = int(request.POST['add_empty_records'])

            myformset = modelformset_factory(StudentType, StudentTypeForm, extra=entries)
            formset = myformset(queryset=StudentType.objects.none())
        elif 'form-0-student_type' in request.POST:  # add records
            formset = myformset(request.POST, queryset=StudentType.objects.none())
            if formset.is_valid():
                formset.save()
                formset = myformset(queryset=StudentType.objects.none())
            else:
                error = "ERROR: Already exists/Invalid/Empty records"
        else:  # delete selected records
            indices = ''.join(request.POST.keys()).replace("form-", '').replace("-check", ' ').split()
            indices = list(list(map(int, indices)))
            indices.sort(reverse=True)
            objects = StudentType.objects.all()
            try:
                for i in indices:
                    objects[i].delete()
            except ProtectedError as p:
                error = str(p)
                error = error[error.find('"') + 1: error.find('"', 4)]
            except:
                error = "ERROR: Student type does not exist/Error performing deletion"

    else:
        formset = myformset(queryset=StudentType.objects.none())
        countform = FieldCountForm()
        deleteform = DeleteForm()

    return render_to_response('student_type.html',
                              {'formset': formset, 'countform': countform, 'deleteform': deleteform,
                               'database': myformset(), 'username': request.user.username,
                               'error': error})


@login_required
@user_passes_test(is_dept_admin)
def subject_type(request):
    error = ''
    entries = 1
    myformset = modelformset_factory(SubjectType, SubjectTypeForm, extra=entries)
    formset = myformset(queryset=SubjectType.objects.none())
    countform = FieldCountForm()
    deleteform = DeleteForm()
    if request.method == 'POST':
        if 'add_empty_records' in request.POST:  # add rows
            entries = int(request.POST['add_empty_records'])

            myformset = modelformset_factory(SubjectType, SubjectTypeForm, extra=entries)
            formset = myformset(queryset=SubjectType.objects.none())
        elif 'form-0-subject_type' in request.POST:  # add records
            formset = myformset(request.POST, queryset=SubjectType.objects.none())
            if formset.is_valid():
                formset.save()
                formset = myformset(queryset=SubjectType.objects.none())
            else:
                error = "ERROR: Already exists/Invalid/Empty records"
        else:  # delete selected records
            indices = ''.join(request.POST.keys()).replace("form-", '').replace("-check", ' ').split()
            indices = map(int, indices)
            indices.sort(reverse=True)
            objects = SubjectType.objects.all()
            try:
                for i in indices:
                    objects[i].delete()
            except ProtectedError as p:
                error = str(p)
                error = error[error.find('"') + 1: error.find('"', 4)]
            except:
                error = "ERROR: Year code does not exist/Error performing deletion"

    else:
        formset = myformset(queryset=SubjectType.objects.none())
        countform = FieldCountForm()
        deleteform = DeleteForm()

    return render_to_response('subject_type.html',
                              {'formset': formset, 'countform': countform, 'deleteform': deleteform,
                               'database': myformset(), 'username': request.user.username,
                               'error': error})


@login_required
@user_passes_test(is_dept_admin)
def subject_delivery_type(request):
    error = ''
    entries = 1
    myformset = modelformset_factory(SubjectDeliveryType, SubjectDeliveryTypeForm, extra=entries)
    formset = myformset(queryset=SubjectDeliveryType.objects.none())
    countform = FieldCountForm()
    deleteform = DeleteForm()
    if request.method == 'POST':
        if 'add_empty_records' in request.POST:  # add rows
            entries = int(request.POST['add_empty_records'])

            myformset = modelformset_factory(SubjectDeliveryType, SubjectDeliveryTypeForm, extra=entries)
            formset = myformset(queryset=SubjectDeliveryType.objects.none())
        elif 'form-0-subject_delivery_type' in request.POST:  # add records
            formset = myformset(request.POST, queryset=SubjectDeliveryType.objects.none())
            if formset.is_valid():
                formset.save()
                formset = myformset(queryset=SubjectDeliveryType.objects.none())
            else:
                error = "ERROR: Already exists/Invalid/Empty records"
        else:  # delete selected records
            indices = ''.join(request.POST.keys()).replace("form-", '').replace("-check", ' ').split()
            indices = map(int, indices)
            indices.sort(reverse=True)
            objects = SubjectDeliveryType.objects.all()
            try:
                for i in indices:
                    objects[i].delete()
            except ProtectedError as p:
                error = str(p)
                error = error[error.find('"') + 1: error.find('"', 4)]
            except:
                error = "ERROR: Year code does not exist/Error performing deletion"

    else:
        formset = myformset(queryset=SubjectDeliveryType.objects.none())
        countform = FieldCountForm()
        deleteform = DeleteForm()

    return render_to_response('subject_delivery_type.html',
                              {'formset': formset, 'countform': countform, 'deleteform': deleteform,
                               'database': myformset(), 'username': request.user.username,
                               'error': error})


@login_required
@user_passes_test(is_dept_admin)
def subject_option(request):
    error = ''
    entries = 1
    myformset = modelformset_factory(SubjectOption, SubjectOptionForm, extra=entries)
    formset = myformset(queryset=SubjectOption.objects.none())
    countform = FieldCountForm()
    deleteform = DeleteForm()
    if request.method == 'POST':
        if 'add_empty_records' in request.POST:  # add rows
            entries = int(request.POST['add_empty_records'])
            myformset = modelformset_factory(SubjectOption, SubjectOptionForm, extra=entries)
            formset = myformset(queryset=SubjectOption.objects.none())
        elif 'form-0-regulation_code' in request.POST:  # add records
            formset = myformset(request.POST, queryset=SubjectOption.objects.none())
            if formset.is_valid():
                formset.save()
                formset = myformset(queryset=SubjectOption.objects.none())
            else:
                error = "ERROR: Already exists/Invalid/Empty records"
        else:  # delete selected records
            indices = ''.join(request.POST.keys()).replace("form-", '').replace("-check", ' ').split()
            indices = map(int, indices)
            indices.sort(reverse=True)
            objects = SubjectOption.objects.all()
            try:
                for i in indices:
                    objects[i].delete()
            except ProtectedError as p:
                error = str(p)
                error = error[error.find('"') + 1: error.find('"', 4)]
            except:
                error = "ERROR: Subject type does not exist/Error performing deletion"

    else:
        formset = myformset(queryset=SubjectOption.objects.none())
        print(myformset().__dict__)
        countform = FieldCountForm()
        deleteform = DeleteForm()

    return render_to_response('subject_option.html',
                              {'formset': formset, 'countform': countform, 'deleteform': deleteform,
                               'database': myformset(), 'username': request.user.username,
                               'error': error})


@login_required
@user_passes_test(is_colg_admin)
def program_structure(request):
    error = ''
    entries = 1
    myformset = modelformset_factory(ProgramStructure, ProgramStructureForm, extra=entries)
    formset = myformset(queryset=ProgramStructure.objects.none())
    countform = FieldCountForm()
    deleteform = DeleteForm()
    if request.method == 'POST':
        if 'add_empty_records' in request.POST:  # add rows
            entries = int(request.POST['add_empty_records'])

            myformset = modelformset_factory(ProgramStructure, ProgramStructureForm, extra=entries)
            formset = myformset(queryset=ProgramStructure.objects.none())
        elif 'form-0-regulation_code' in request.POST:  # add records
            formset = myformset(request.POST, queryset=ProgramStructure.objects.none())
            if formset.is_valid():
                formset.save()
                formset = myformset(queryset=ProgramStructure.objects.none())
            else:
                error = "ERROR: Already exists/Invalid/Empty records"
        else:  # delete selected records
            indices = ''.join(request.POST.keys()).replace("form-", '').replace("-check", ' ').split()
            indices = map(int, indices)
            indices.sort(reverse=True)
            objects = ProgramStructure.objects.all()
            try:
                for i in indices:
                    objects[i].delete()
            except ProtectedError as p:
                error = str(p)
                error = error[error.find('"') + 1: error.find('"', 4)]
            except:
                error = "ERROR: Regalation Code does not exist/Error performing deletion"

    else:
        formset = myformset(queryset=ProgramStructure.objects.none())
        countform = FieldCountForm()
        deleteform = DeleteForm()

    return render_to_response('program_structure.html',
                              {'formset': formset, 'countform': countform, 'deleteform': deleteform,
                               'database': myformset(), 'username': request.user.username,
                               'error': error})

@login_required
@user_passes_test(is_dept_admin)
def course_registration(request):
    entries = 1
    myformset = modelformset_factory(Student, StudentForm, extra=entries)
    course_code = CourseOffered.objects.all()[0]
    course_reg_objects = CourseRegistration.objects.filter(course_code=course_code)
    registered_candidates = map(lambda x: x.student_reg_no, course_reg_objects)
    if registered_candidates:
        unregistered_candidates = Student.objects.exclude(student_reg_no__in=registered_candidates)
    else:
        unregistered_candidates = Student.objects.all()
    courses = CourseOffered.objects.all()
    courses_list=map(lambda x: x.course_code, courses)
    course_form = create_course_selection_form(courses, course_code.course_code)
    unreg_form = None
    reg_form = None
    if request.method == 'POST':
        if "course" in request.POST:
            course_code_input = request.POST["course"]
            if type(course_code_input).__name__ == "list":
                course_code_input = course_code_input[0]
            course_code = CourseOffered.objects.get(course_code=int(course_code_input))
            course_form = create_course_selection_form(courses, course_code.course_code)
            course_reg_objects = CourseRegistration.objects.filter(course_code=course_code)
            registered_candidates = map(lambda x: x.student_reg_no, course_reg_objects)
            if registered_candidates:
                unregistered_candidates = Student.objects.exclude(student_reg_no__in=registered_candidates)
            else:
                unregistered_candidates = Student.objects.all()
        keys = request.POST.keys()
        if "course" in keys:
            keys.remove("course")
        if keys:
            submitted_form = keys[0][4]
            indices = [key.split('-')[1] for key in keys]
            unreg_indices = filter(lambda x: "form1" in x, indices)
            reg_indices = filter(lambda x: "form2" in x, indices)
            unreg_indices = map(int, indices)
            reg_indices = map(int, indices)
            unreg_indices.sort(reverse=True)
            reg_indices.sort(reverse=True)
            unregistered_candidates = sorted(unregistered_candidates, key=lambda x:x.student_reg_no)
            registered_candidates = sorted(registered_candidates, key=lambda x:x.student_reg_no)
            if submitted_form == "1":
                for i in unreg_indices:
                    candidate = unregistered_candidates[i]
                    CourseRegistration.objects.create(student_reg_no=candidate, course_code=course_code)
            else:
                for i in reg_indices:
                    candidate = registered_candidates[i]
                    CourseRegistration.objects.get(student_reg_no=candidate, course_code=course_code).delete()

            registered_candidates = map(lambda x: x.student_reg_no,
                                        CourseRegistration.objects.filter(course_code=course_code))
            if registered_candidates:
                unregistered_candidates = Student.objects.exclude(student_reg_no__in=registered_candidates)
            else:
                unregistered_candidates = Student.objects.all()

    if not unregistered_candidates:
        unreg_form = myformset(queryset=Student.objects.none(), prefix='form1')
    else:
        unreg_form = myformset(queryset=unregistered_candidates, prefix='form1')
    if not registered_candidates:
        reg_form = myformset(queryset=Student.objects.none(), prefix='form2')
    else:
        reg_form = myformset(queryset=Student.objects.filter(student_reg_no__in=registered_candidates), prefix='form2')
    return render_to_response('course_registration.html', {'selection_form' : course_form, 'unreg_formset': unreg_form,
                                                           'reg_formset': reg_form, 'error': ''})

@login_required
@user_passes_test(is_colg_admin)
def feedback_type(request):
    error = ''
    entries = 1
    myformset = modelformset_factory(FeedbackType, FeedbackTypeForm, extra=entries)
    formset = myformset(queryset=FeedbackType.objects.none())
    countform = FieldCountForm()
    deleteform = DeleteForm()
    if request.method == 'POST':
        if 'add_empty_records' in request.POST:  # add rows
            entries = int(request.POST['add_empty_records'])

            myformset = modelformset_factory(FeedbackType, FeedbackTypeForm, extra=entries)
            formset = myformset(queryset=FeedbackType.objects.none())
        elif 'form-0-cycle_no' in request.POST:  # add records
            formset = myformset(request.POST, queryset=FeedbackType.objects.none())
            if formset.is_valid():
                formset.save()
                formset = myformset(queryset=FeedbackType.objects.none())
            else:
                error = "ERROR: Already exists/Invalid/Empty records"
        else:  # delete selected records
            indices = ''.join(request.POST.keys()).replace("form-", '').replace("-check", ' ').split()
            indices = map(int, indices)
            indices.sort(reverse=True)
            objects = FeedbackType.objects.all()
            try:
                for i in indices:
                    objects[i].delete()
            except ProtectedError as p:
                error = str(p)
                error = error[error.find('"') + 1: error.find('"', 4)]
            except:
                error = "ERROR: Cycle number  does not exist/Error performing deletion"

    else:
        formset = myformset(queryset=FeedbackType.objects.none())
        countform = FieldCountForm()
        deleteform = DeleteForm()

    return render_to_response('feedback_type.html',
                              {'formset': formset, 'countform': countform, 'deleteform': deleteform,
                               'database': myformset(), 'username': request.user.username,
                               'error': error})

@login_required
@user_passes_test(is_student)
def submit_feedback(request):
    error=''
    student_id = request.user.username
    student = Student.objects.get(student_reg_no=student_id)

    course_id = request.GET['course']
    cycle_no = request.GET['cycle']


    if request.method == 'POST':
        print request.POST
        cycle = FeedbackType.objects.get(cycle_no=cycle_no)
        course = CourseOffered.objects.get(course_code=course_id)
        feedback_assignment = CourseFeedbackAssignment.objects.get(student_reg_no__student_reg_no__student_reg_no=student,
                                                                   course_code__course_code__course_code=course_id,
                                                                   cycle_no__cycle_no=cycle_no)
        feedback_assignment.is_given = 1
        weighting = feedback_assignment.feedback_weighting
        feedback_assignment.save()

        feedback_comment_object = FeedbackCommentLog(course_code=course,
                                                     cycle_no=cycle,
                                                     feedback_weighting=weighting,
                                                     feedback_comments=request.POST['comments'],
                                                     )

        feedback_comment_object.save()
        responses = request.POST.keys()
        responses.remove('comments')

        feedback_rating_aggregate = {'course_code': course,
                                            'cycle_no': cycle,
                                            'rating_5_count_1': 0,
                                            'rating_5_count_2': 0,
                                            'rating_4_count_1': 0,
                                            'rating_4_count_2': 0,
                                            'rating_3_count_1': 0,
                                            'rating_3_count_2': 0,
                                            'rating_2_count_1': 0,
                                            'rating_2_count_2': 0,
                                            'rating_1_count_1': 0,
                                            'rating_1_count_2': 0,
                                            }

        for response in responses:
            answer = request.POST[response]
            FeedbackRatingLog.objects.create(feedback_no=feedback_comment_object,
                                             course_code=feedback_comment_object,
                                             cycle_no=feedback_comment_object,
                                             question_no=int(response),
                                             feedback_weighting=weighting,
                                             rating_answer=answer)
            feedback_rating_aggregate['rating_' + answer + '_count_' + str(weighting)] += 1

        FeedbackRatingAggregate.objects.create(**feedback_rating_aggregate)
        return HttpResponseRedirect(reverse('view_courses'))

    elif request.method == "GET":
        try:
            feedback_assignment = CourseFeedbackAssignment.objects.filter(
                student_reg_no__student_reg_no__student_reg_no=student,
                course_code__course_code__course_code=course_id,
                cycle_no__cycle_no=cycle_no)
            if feedback_assignment.is_given == 1:
                raise ValueError('Already given')
            questions = FeedbackQuestion.objects.filter(cycle_no__cycle_no=cycle_no)
        except:
            return HttpResponseRedirect(reverse('view_courses'))

        return render_to_response('submit_feedback.html', {'error': error, 'questions': questions,
                                                           'course': CourseOffered.objects.get(
                                                               course_code=course_id).course_name})





@login_required
@user_passes_test(is_student)
def submit_comment(request):
    error=''
    student_id = request.user.username
    student = Student.objects.get(student_reg_no=student_id)
    registered_courses = CourseRegistration.objects.filter(student_reg_no=student)
    course_names = [course.course_code.course_name for course in registered_courses]
    questions = FeedbackQuestion.objects.all()

    return render_to_response('submit_comment.html', {'error': error, 'courses': course_names})


@login_required
@user_passes_test(is_colg_admin)
def feedback_question(request):
    error = ''
    entries = 1
    myformset = modelformset_factory(FeedbackQuestion, FeedbackQuestionForm, extra=entries)
    formset = myformset(queryset=FeedbackQuestion.objects.none())
    countform = FieldCountForm()
    deleteform = DeleteForm()
    if request.method == 'POST':
        if 'add_empty_records' in request.POST:  # add rows
            entries = int(request.POST['add_empty_records'])
            myformset = modelformset_factory(FeedbackQuestion, FeedbackQuestionForm, extra=entries)
            formset = myformset(queryset=FeedbackQuestion.objects.none())
        elif 'form-0-cycle_no' in request.POST:  # add records
            formset = myformset(request.POST, queryset=FeedbackQuestion.objects.none())
            if formset.is_valid():
                formset.save()
                formset = myformset(queryset=FeedbackQuestion.objects.none())
            else:
                error = "ERROR: Already exists/Invalid/Empty records"
        else:  # delete selected records
            indices = ''.join(request.POST.keys()).replace("form-", '').replace("-check", ' ').split()
            indices = map(int, indices)
            indices.sort(reverse=True)
            objects = FeedbackQuestion.objects.all()
            try:
                for i in indices:
                    objects[i].delete()
            except ProtectedError as p:
                error = str(p)
                error = error[error.find('"') + 1: error.find('"', 4)]
            except:
                error = "ERROR in deletion"

    else:
        formset = myformset(queryset=FeedbackQuestion.objects.none())
        countform = FieldCountForm()
        deleteform = DeleteForm()

    return render_to_response('feedback_question.html',
                              {'formset': formset, 'countform': countform, 'deleteform': deleteform,
                               'database': myformset(), 'username': request.user.username,
                               'error': error})


@login_required
@user_passes_test(is_dept_admin)
def manage_course_feedback_assignment(request):
    entries = 1

    course_code, cycle_no  = map(int, request.GET['manage'].split('-'))
    cycle = FeedbackType.objects.get(cycle_no=int(cycle_no))

    students = CourseRegistration.objects.filter(course_code__course_code=course_code)

    course_feedback_object = CourseFeedbackAssignment.objects.filter(course_code__course_code=course_code,
                                                                     cycle_no__cycle_no=cycle_no)[0]

    high_weightage_candidates = map(lambda x: x.student_reg_no,
                                    CourseFeedbackAssignment.objects.filter(feedback_weighting=2,
                                                                            course_code__course_code__course_code=course_code,
                                                                            cycle_no=cycle).order_by('student_reg_no__student_reg_no__student_reg_no'))
    low_weightage_candidates = map(lambda x: x.student_reg_no,
                                   CourseFeedbackAssignment.objects.filter(feedback_weighting=1,
                                                                           course_code__course_code__course_code=course_code,
                                                                           cycle_no=cycle).order_by('student_reg_no__student_reg_no__student_reg_no'))

    new_candidates = CourseRegistration.objects.filter(course_code__course_code=course_code).exclude(student_reg_no__student_reg_no__in= low_weightage_candidates + high_weightage_candidates)

    for candidate in new_candidates:
        CourseFeedbackAssignment.objects.create(student_reg_no=candidate,
                                                course_code=candidate,
                                                cycle_no=cycle,
                                                start_date=course_feedback_object.start_date,
                                                end_date=course_feedback_object.end_date
                                                )
    high_weightage_candidates = map(lambda x: x.student_reg_no,
                                    CourseFeedbackAssignment.objects.filter(feedback_weighting=2,
                                                                            course_code__course_code__course_code=course_code,
                                                                            cycle_no=cycle).order_by('student_reg_no__student_reg_no__student_reg_no'))

    candidates_given = map(lambda x: x.student_reg_no,
                                    CourseFeedbackAssignment.objects.filter(is_given=1,
                                                                            course_code__course_code__course_code=course_code,
                                                                            cycle_no=cycle).order_by('student_reg_no__student_reg_no__student_reg_no'))

    candidates_not_given = map(lambda x: x.student_reg_no,
                                        CourseFeedbackAssignment.objects.filter(is_given=0,
                                                                                course_code__course_code__course_code=course_code,
                                                                                cycle_no=cycle).order_by('student_reg_no__student_reg_no__student_reg_no'))

    if request.method == 'POST':


        #Course from post
        course_code = request.POST['course_code']
        cycle_no = request.POST['cycle_no']


        keys = request.POST.keys()
        if keys:
            keys.remove('course_code')
            keys.remove('cycle_no')
            submitted_form = keys[0][4]
            indices = [key.split('-')[1] for key in keys]
            indices = map(int, indices)
            indices.sort(reverse=True)

            if submitted_form == "1":
                for i in indices:
                    candidate = low_weightage_candidates[i]
                    CourseFeedbackAssignment.objects.filter(
                        course_code__course_code__course_code=course_code,
                        cycle_no__cycle_no=cycle_no,
                        student_reg_no__student_reg_no__student_reg_no=candidate
                    ).update(feedback_weighting=2)
            elif submitted_form == "2":
                for i in indices:
                    candidate = high_weightage_candidates[i]
                    CourseFeedbackAssignment.objects.filter(
                        course_code__course_code__course_code=course_code,
                        cycle_no__cycle_no=cycle_no,
                        student_reg_no__student_reg_no__student_reg_no=candidate
                    ).update(feedback_weighting=1)
            elif submitted_form == "3":
                for i in indices:
                    candidate = candidates_not_given[i]
                    CourseFeedbackAssignment.objects.filter(
                        course_code__course_code__course_code=course_code,
                        cycle_no__cycle_no=cycle_no,
                        student_reg_no__student_reg_no__student_reg_no=candidate
                    ).update(is_given=1)
            else:
                for i in indices:
                    candidate = candidates_given[i]
                    CourseFeedbackAssignment.objects.filter(
                        course_code__course_code__course_code=course_code,
                        cycle_no__cycle_no=cycle_no,
                        student_reg_no__student_reg_no__student_reg_no=candidate
                    ).update(is_given=0)

    print CourseFeedbackAssignment.objects.filter(is_given=0,
                                                 course_code__course_code=course_code,
                                                 cycle_no__cycle_no=cycle_no)

    return render_to_response('course_feedback_assignment.html', {
        'low': CourseFeedbackAssignment.objects.filter(feedback_weighting=1,
                                                       course_code__course_code=course_code,
                                                       cycle_no__cycle_no=cycle_no)
                              .values('student_reg_no__student_reg_no__student_reg_no')
                              .order_by('student_reg_no__student_reg_no__student_reg_no'),
        'high': CourseFeedbackAssignment.objects.filter(feedback_weighting=2,
                                                        course_code__course_code=course_code,
                                                        cycle_no__cycle_no=cycle_no)
                              .values('student_reg_no__student_reg_no__student_reg_no')
                              .order_by('student_reg_no__student_reg_no__student_reg_no'),
        'not_given': CourseFeedbackAssignment.objects.filter(is_given=0,
                                                             course_code__course_code=course_code,
                                                             cycle_no__cycle_no=cycle_no)
                              .values('student_reg_no__student_reg_no__student_reg_no')
                              .order_by('student_reg_no__student_reg_no__student_reg_no'),
        'given': CourseFeedbackAssignment.objects.filter(is_given=1,
                                                         course_code__course_code=course_code,
                                                         cycle_no__cycle_no=cycle_no)
                            .values('student_reg_no__student_reg_no__student_reg_no')
                            .order_by('student_reg_no__student_reg_no__student_reg_no'),
        'course_code': course_code,
        'cycle_no': cycle_no,
        'error': ''})


def create_course_feedback_assignment(request):

    error = ''
    course_feedback_objects = CourseFeedbackAssignment.objects.values('course_code__course_code__course_code', 'cycle_no', 'start_date', 'end_date').distinct()
    print course_feedback_objects
    deleteform = DeleteForm()
    print request.POST
    if request.method == 'POST':
        if 'course_code' in request.POST: # add records
            try:
                course_code = CourseOffered.objects.get(course_code=request.POST['course_code'])
                students = CourseRegistration.objects.filter(course_code=course_code)
                start_date = request.POST['start_date']
                end_date = request.POST['end_date']
                cycle_no = FeedbackType.objects.get(cycle_no=request.POST['cycle_no'])
                for s in students:
                    CourseFeedbackAssignment.objects.create(course_code=s,
                                                            student_reg_no=s,
                                                            cycle_no=cycle_no,
                                                            start_date=start_date,
                                                            end_date=end_date)

            except Exception as e:
                print e
                error = "ERROR: Already exists/Empty records/Invalid Data or Dates"

        else: # delete selected records
            print request.POST
            indices = ''.join(request.POST.keys()).replace("form-", '').replace("-check", ' ').split()
            indices = list(map(int, indices))
            indices.sort(reverse=True)

            print indices
            try:
                for i in indices:
                    obj = course_feedback_objects[i]
                    print obj
                    CourseFeedbackAssignment.objects.filter(
                        course_code__course_code__course_code=obj['course_code__course_code__course_code'],
                        cycle_no__cycle_no=obj['cycle_no']).delete()

            except ProtectedError as e:
                error = e
                print e
            except Exception as e:
                print e
                error = "ERROR: Faculty code does not exist/Error performing deletion"

    else:
        if 'manage' in request.GET:
            print request.GET
            return HttpResponseRedirect(reverse('manage')+ '?manage=' + request.GET['manage'])
        deleteform = DeleteForm()


    return render_to_response('course_feedback_view.html', {
                            'deleteform': deleteform,
                            'form': CourseFeedbackAssignmentForm(),
                            'database': course_feedback_objects,
                            'username': request.user.username,
                            'error': error})


def view_courses(request):
    given_courses = CourseFeedbackAssignment.objects.values('course_code__course_code__course_name','cycle_no__cycle_no','start_date','end_date').filter(student_reg_no__student_reg_no__student_reg_no = request.user.username,is_given=1)
    not_given_courses = CourseFeedbackAssignment.objects.values('course_code__course_code__course_name','course_code__course_code__course_code','cycle_no__cycle_no','start_date','end_date').filter(
        student_reg_no__student_reg_no__student_reg_no=request.user.username, is_given=0)


    if request.method=='POST':
        return HttpResponseRedirect('/feedback/submit_feedback?course=' + request.POST["course_code"] + '&cycle=' + request.POST["cycle_no"])


    return render_to_response('view_courses.html',
                              {
                                  'given_courses' : given_courses,
                                  'not_given_courses' : not_given_courses
                              })

@login_required
@user_passes_test(is_faculty)
def faculty_home_page(request):
    courses = CourseOffered.objects.filter(faculty_name__faculty_code = request.user.username)
    return render_to_response('faculty_home_page.html',
                                {
                                    'courses' : courses
                                })