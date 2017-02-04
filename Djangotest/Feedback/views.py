from django.http import HttpResponse
#from .models import *
from .forms import *
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import datetime


def login_view(request):
    print type(request)
    if request.POST:
        username = request.POST['id_no']
        password = request.POST['crypt_password']
        user = authenticate(username = username, password=password)
        # user = form.__dict__['data']['id_no']
#        try:
#            Users.objects.get(id_no=user)
#            request.session[user] = str(datetime.datetime.now())
#            print request.session[user]
#            return HttpResponseRedirect('/feedback/')
#        except:
#            return HttpResponse("You are not a registered user")
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/feedback/')
        else:
            return HttpResponse("You are not a registered user")
    else:
        form = LoginForm()
    return render_to_response("login.htm", {'form': form })

def logout_view(request):
    logout(request)

def index(request):
    return HttpResponse("Hello, world. You're at the feedback index.")
