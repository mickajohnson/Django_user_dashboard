from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url('^$', views.index, name="index"),
    url('^signin/$', views.signin, name="signin"),
    url('^authenticate/$', views.authenticate, name="authenticate"),
    url('^register/$', views.register, name="register"),
    url('^register_add/$', views.register_add, name="register_add"),
    url('^dashboard/$', views.dashboard, name="dashboard"),
    url('^dashboard/admin/$', views.dashboard_admin, name="dashboard_admin"),
    url('^logout/$', views.logout, name="logout"),
    url('^users/show/(?P<id>\d+)/$', views.show, name="show"),
    url('^users/message/(?P<id>\d+)/$', views.message, name="message"),
    url('^users/message/(?P<user_id>\d+)/delete/(?P<message_id>\d+)$', views.delete_message, name="delete_message"),
    url('^users/comment/(?P<user_id>\d+)/delete/(?P<comment_id>\d+)/$', views.delete_comment, name="delete_comment"),
    url('^users/comment/(?P<user_id>\d+)/(?P<message_id>\d+)/$', views.comment, name="comment"),
    url('^users/edit/(?P<id>\d+)/$', views.edit_admin, name="edit_admin"),
    url('^users/show/edit/$', views.edit, name="edit"),
    url('^users/show/update/(?P<id>\d+)/$', views.update, name="update"),
    url('^users/new/$', views.new, name="new"),
]
