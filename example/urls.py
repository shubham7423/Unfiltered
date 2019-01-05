from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from .import views

app_name = 'example'
urlpatterns = [
    path('login',views.index,name="index"),
    path('',views.welcome,name="welcome"),
    path('register/',views.register,name="register"),
    path('logout',views.log_out,name="log_out"),
    path('change_password',views.change_password,name="change_password"),
    path('add_post',views.create_post,name="create_post"),

    path('dashboard',views.dashboard,name="dashboard"),
    #path('(<post_id>[0-9]+)/',views.detail,name="detail"),
    url(r'^(?P<post_id>[0-9]+)/$', views.detail, name='detail'),
    #path('add_comment',views.add_comment,name="add_comment"),
    url(r'^(?P<post_id>[0-9]+)/add_comment$', views.add_comment, name='add_comment'),
    url(r'^(?P<post_id>[0-9]+)/delete_post$', views.delete_post, name='delete_post'),
    url(r'^(?P<comment_id>[0-9]+)/delete_comment$', views.delete_comment, name='delete_comment'),
    url(r'^(?P<post_id>[0-9]+)/edit_post$', views.edit_post, name='edit_post'),
    url(r'^(?P<cat>[a-z]+)/$', views.detailed_cat, name='detailed_cat'),
]
