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
                logout(request)
                login(request, user)
                if not request.session.session_key in s:
                    s[request.session.session_key] = username
                return HttpResponseRedirect('/feedback/')
            else:
                print("not authenticated")
                return HttpResponse(request.user.is_authenticated())
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
        form2=RegistrationForm()
    return render_to_response("login.htm", {'form': form,'form2':  form2 })

def logout_view(request):
    del request.session[request.session.session_key]
    logout(request)

def index(request):
    print(s[request.session.session_key])
    return HttpResponse("hello " + str(s[request.session.session_key]))


