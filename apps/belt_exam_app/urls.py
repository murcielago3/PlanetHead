from django.conf.urls import url
from . import views           # This line is new!
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^create$', views.create),
    url(r'^join(?P<id>\d+)$', views.join),
    url(r'^cancel(?P<id>\d+)$', views.cancel),
    url(r'^process(?P<user_id>\d+)$', views.process),
    url(r'^display$', views.displaypage),
    url(r'^logout$', views.logout),
    url(r'^delete(?P<job_id>\d+)$', views.deleteJobs),
    url(r'^edit(?P<id>\d+)$', views.edit),
    url(r'^view(?P<id>\d+)$', views.view),
    url(r'^update(?P<job_id>\d+)$', views.update_job),# This line has changed! Notice that urlpatterns is a list, the comma is in
]                            # anticipation of all the routes that will be coming soon
