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
        username = request.POST['id_no']
        password = request.POST['crypt_password']
        s[request.session.session_key]=username
        user = authenticate(username = username, password=password)

        if not user is None:
            login(request, user)
            return HttpResponseRedirect('/feedback/')
        else:
            print("not authenticated")
            return HttpResponse(request.user.is_authenticated())
    else:
        form = LoginForm()

    return render_to_response("login.htm", {'form': form })

def logout_view(request):
    logout(request)

def index(request):
    print(s[request.session.session_key])
    return HttpResponse("hello " + str(s[request.session.session_key]))


