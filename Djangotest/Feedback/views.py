from django.http import HttpResponse
#from .models import *
from .forms import *
from django.forms import modelformset_factory
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views import View
from django.db.models import ProtectedError
from django.utils.functional import curry
from functools import partial, wraps


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
                    return HttpResponseRedirect('/feedback/submit_feedback')
                else:
                    return HttpResponseRedirect('/feedback')
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
    return HttpResponseRedirect('login')


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
        header = 'admin_header.html'
    elif is_dept_admin(request.user):
        header = 'dept_admin_header.html'
    elif is_student(request.user):
        header = 'student_header.html'
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
                    return HttpResponseRedirect("login")
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
    registered_courses = CourseRegistration.objects.filter(student_reg_no=student)
    course_names = [course.course_code.course_name for course in registered_courses]
    course_count = len(course_names)
    questions = FeedbackQuestion.objects.all()
    question_count = len(questions)
    if request.method == 'POST':
        keys = request.POST.keys()
        print (course_count, question_count)
        for i in range(course_count):
            course_name = course_names[i]
            course_ratings = {}
            for j in range(question_count):
                rating = request.POST[keys[i*course_count + j]][0]
                course_ratings[rating] = course_ratings.get(rating, 0) + 1
            print course_name, course_ratings


    return render_to_response('submit_feedback.html', {'error': error, 'questions':questions, 'courses': course_names})


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
def course_feedback_assignment(request):
    entries = 1

    courses = map(lambda x: x.course_code, CourseOffered.objects.all())
    cycles = map(lambda x: x.cycle_no, FeedbackType.objects.all())
    course_feedback_assignment_form = None

    students = Student.objects.filter(course_code=courses[0])


    if request.method == 'POST':

        selected_course = request.POST["selected_course"]
        students = Student.objects.filter(course_code=selected_course)

        if "course" in request.POST:
            course_code_input = request.POST["course"]
            cycle_no = request.POST["cycle_no"]
            if type(course_code_input).__name__ == "list":
                course_code_input = course_code_input[0]
            course_code = CourseOffered.objects.get(course_code=int(course_code_input))
            cycle = FeedbackType.objects.get(cycle_no=int(cycle_no))

            
            low_weightage = students
            high_weightage = None

        keys = request.POST.keys()
        if "course" in keys:
            keys.remove("course")
        if keys:
            submitted_form = keys[0][4]
            indices = [key.split('-')[1] for key in keys]
            low_weightage_indices = filter(lambda x: "form1" in x, indices)
            high_weightage_indices = filter(lambda x: "form2" in x, indices)
            low_weightage_indices = map(int, indices)
            high_weightage_indices = map(int, indices)
            low_weightage_indices.sort(reverse=True)
            high_weightage_indices.sort(reverse=True)
            low_weightage_candidates = sorted(low_weightage_candidates, key=lambda x:x.student_reg_no)
            high_weightage_candidates = sorted(high_weightage_candidates, key=lambda x:x.student_reg_no)
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


    return render_to_response('course_feedback_assignment.html', {
        'assgn_form' : course_feedback_assignment_form,
        'error': ''})
