from django.http import HttpResponse
#from .models import *
from .forms import *
from django.forms import modelformset_factory
from threading import current_thread
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
import datetime

s = SessionStore()
def login_view(request):
    if request.POST:
        if 'crypt_password' in request.POST:
            form = LoginForm(request)
            username = request.POST['id_no']
            password = request.POST['crypt_password']
            #if request.session.session_key is None:
            #    return HttpResponse("You are already logged in as {0}".format(request.user.username))
            user = authenticate(username=username, password=password)

            print(s.__dict__)
            if not user is None:
                login(request, user)
                if not request.user.username in s:
                    s[request.user.username] = request.session.session_key
                return HttpResponseRedirect('/feedback/')
            else:
                return HttpResponse("Invalid Authentication")
        else:
            form2 = RegistrationForm(request)
            username=request.POST['id_no']
            password1=request.POST['password1']
            password2=request.POST['password2']
            if password1!=password2:
                return HttpResponse("Passwords Mismatch")
            if len(username)!=10:
                return HttpResponse("Invalid Username")
            User.objects.create_user(username.upper(),'example@gmail.com',password1).save()
            return HttpResponse("<h1>Successfully Registered</h1>")
    else:
        form = LoginForm()
        form2 = RegistrationForm()
    return render_to_response("login.htm", {'form': form,'form2':  form2 })

def logout_view(request):
    del s[request.user.username]
    logout(request)
    return HttpResponse("Successfully Loggedout")

@login_required
def index(request):
    print(s[request.user.username])
    return HttpResponse("hello " + request.user.username + str(s[request.user.username]))

#@login_required
def admin(request):
    return render_to_response("admin.htm")

def academic_year(request):
    entries = 1
    myformset = modelformset_factory(AcademicYear, AcademicYearForm, extra=entries)
    countform = FieldCountForm()
    deleteform = DeleteForm()
    if 'key' in request.POST:
        AcademicYear.objects.get(academic_year_code=int(request.POST['key'])).delete()
        return HttpResponse(AcademicYear.objects.all())
    if 'count' in request.POST:
        entries = int(request.POST['count'])
        myformset = modelformset_factory(AcademicYear, AcademicYearForm, extra=entries)
    if 'form-INITIAL_FORMS' in request.POST:
        formset = myformset(request.POST, queryset=AcademicYear.objects.none())
        if formset.is_valid():
            formset.save()
            formset = myformset(queryset=AcademicYear.objects.none())
        else:
            return HttpResponse("WRONG DATA")
    else:
        formset = myformset(queryset=AcademicYear.objects.none())
        countform = FieldCountForm()
        deleteform = DeleteForm()

    return render_to_response('academic_year.htm', {'formset': formset, 'countform': countform, 'deleteform': deleteform})

def display(request):
    form = modelformset_factory(AcademicYear, AcademicYearForm)()
    return render_to_response('display.html', {'display': form})