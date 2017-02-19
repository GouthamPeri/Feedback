from django.conf.urls import url

from . import views
#from .views import (reporter_create)
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login',views.login_view),
    url(r'^logout',views.logout_view),
    url(r'^admin', views.admin),
    url(r'^dept_admin', views.dept_admin),
    url(r'^display', views.display),
    url(r'^academic_year', views.academic_year),
    url(r'^faculty', views.faculty),
    url(r'^change_password', views.change_password),
    url(r'^regulation', views.regulation),
    url(r'^department', views.department),
    url(r'^add_program', views.add_program),
    url(r'^course_offered', views.course_offered),
    url(r'^student_type', views.student_type)
]