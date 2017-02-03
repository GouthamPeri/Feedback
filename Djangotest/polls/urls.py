from django.conf.urls import url

from . import views
#from .views import (reporter_create)
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create/$',views.create)
]