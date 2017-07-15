from django.conf.urls import url
from django.views.i18n import javascript_catalog

from . import views
#from .views import (reporter_create)
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$',views.login_view,name='login'),
    url(r'^logout/$',views.logout_view,name='logout'),
    url(r'^admin', views.admin_header,name='admin'),
    url(r'^dept_admin/$', views.dept_admin_header,name='dept_admin'),
    url(r'^student_header/$', views.student_header,name='student_header'),
    url(r'^academic_year/$', views.academic_year,name='academic_year'),
    url(r'^faculty/$', views.faculty,name='faculty'),
    url(r'^change_password/$', views.change_password,name='change_password'),
    url(r'^regulation/$', views.regulation,name='regulation'),
    url(r'^department/$', views.department,name='department'),
    url(r'^program/$', views.add_program,name='program'),
    url(r'^course_offered/$', views.course_offered, name='course_offered'),
    url(r'^student/$', views.student,name='student'),
    url(r'^student_type/$', views.student_type,name='student_type'),
    url(r'^subject_type/$', views.subject_type,name='subject_type'),
    url(r'^program_structure/$', views.program_structure,name='program_structure'),
    url(r'^subject_delivery_type/$', views.subject_delivery_type,name='subject_delivery_type'),
    url(r'^subject_option/$', views.subject_option,name='subject_option'),
    url(r'^course_registration/$', views.course_registration, name='course_registration'),
    url(r'^admin/js/jsi18n.js/$', javascript_catalog),
    url(r'^feedback_type/$', views.feedback_type,name='feedback_type'),
    url(r'^submit_feedback/$', views.submit_feedback, name='submit_feedback'),
    url(r'^feedback_question/$', views.feedback_question,name='feedback_question'),
    url(r'^create_course_feedback/$', views.create_course_feedback_assignment,name='create_course_feedback'),
    url(r'^manage_course_feedback/$', views.manage_course_feedback_assignment, name="manage"),
    url(r'^view_courses/$', views.view_courses,name='view_courses'),
    url(r'^faculty_home_page/$', views.faculty_home_page,name='faculty_home_page'),
    url(r'^view_feedback/$', views.view_feedback, name='view_feedback'),
    url(r'^view_department_feedback/$', views.view_department_feedback, name='view_department_feedback')
]