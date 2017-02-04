from django.http import HttpResponse
#from .models import *
from .forms import *
from threading import current_thread
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import datetime

requests = {}
s = SessionStore()
def login_view(request):
    if request.POST:
        if 'crypt_password' in request.POST:
            form = LoginForm(request)
            username = request.POST['id_no']
            password = request.POST['crypt_password']
            user = authenticate(username = username, password=password)

            if not user is None:
                login(request, user)
                if not s.has_key(request.user.username):
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
def index(request):
    print(s[request.user.username])
    return HttpResponse("hello " + request.user.username + str(s[request.user.username]))


