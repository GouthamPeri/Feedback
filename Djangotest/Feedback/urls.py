from django.conf.urls import url

from . import views
#from .views import (reporter_create)
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login',views.login_view),
    url(r'^logout',views.logout_view),
    url(r'^test', views.test_multiple),
    url(r'^admin', views.admin),
]