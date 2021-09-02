from django.contrib import admin
from django.http import request
from django.urls import path
from . import views

urlpatterns = [
    path('',views.login,name='login'),
    path('register',views.register,name="register"),
    path('index/',views.index,name='index'),
    path('otp/',views.otp,name='otp'),
    path('profile/',views.profile,name='profile'),
    path('logout/',views.logout,name='logout'),
    path('forgot pass1/',views.forgot_pass1,name='forgot pass1'),
    path('forgot pass2/',views.forgot_pass2,name='forgot pass2'),
    path('forgot pass3/',views.forgot_pass3,name='forgot pass3'),
    path('table/',views.table,name='table'),
    path('add-event/',views.add_event,name='add-event'),
    path('all-event/',views.all_event,name='all-event'),
    path('edit-event/<int:pk>',views.edit_event,name='edit-event'),
    path('delete-event/<int:pk>',views.delete_event,name='delete-event'),
    path('add-member/',views.add_member,name='add-member'),
]
