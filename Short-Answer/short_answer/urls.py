from django.conf.urls import url
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^shome/$', views.shome, name='student_home'),
    url(r'^thome/$', views.thome, name='teacher_home'),
    url(r'^test/$', views.test, name='student_test'),
    url(r'^test/viewscore/$', views.viewscore, name='view_score'),
    url(r'^question/$', views.question, name='question'),
    url(r'^addqs/$', views.addqs, name='addqs'),
    url(r'^logout/$', views.user_logout, name='logout'),


]
