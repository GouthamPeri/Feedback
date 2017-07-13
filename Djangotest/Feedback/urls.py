from django.conf.urls import url
from django.views.i18n import javascript_catalog

from . import views
#from .views import (reporter_create)
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login',views.login_view),
    url(r'^logout',views.logout_view),
    url(r'^admin', views.admin_header),
    url(r'^dept_admin', views.dept_admin_header),
    url(r'^student_header', views.student_header),
    url(r'^academic_year', views.academic_year),
    url(r'^faculty', views.faculty),
    url(r'^change_password', views.change_password),
    url(r'^regulation', views.regulation),
    url(r'^department', views.department),
    url(r'^program$', views.add_program),
    url(r'^course_offered', views.course_offered),
    url(r'^student$', views.student),
    url(r'^student_type$', views.student_type),
    url(r'^subject_type', views.subject_type),
    url(r'^program_structure', views.program_structure),
    url(r'^subject_delivery_type', views.subject_delivery_type),
    url(r'^subject_option', views.subject_option),
    url(r'^course_registration', views.course_registration),
    url(r'^admin/js/jsi18n.js/$', javascript_catalog),
    url(r'^feedback_type', views.feedback_type),
    url(r'^submit_feedback', views.submit_feedback),
    url(r'^submit_comment', views.submit_comment),
    url(r'^feedback_question', views.feedback_question),
    url(r'^create_course_feedback', views.create_course_feedback_assignment),
    url(r'^manage_course_feedback', views.manage_course_feedback_assignment, name="manage"),
    url(r'^view_courses', views.view_courses)
]