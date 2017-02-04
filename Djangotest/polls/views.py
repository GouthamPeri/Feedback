from django.http import HttpResponse
from .models import Reporter1
from .forms import ReporterForm
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
def create(request):
    if request.POST:
        form=ReporterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/polls/')
    else:
        form=ReporterForm()
    return render_to_response("people.html",{'form':form})

def index(request):
     return HttpResponse("Hello, world. You're at the polls index.")