
from django.http import request
from django.urls import path
from . import views

urlpatterns = [
	path('',views.flat_login,name='flat-login'),
	path('flat-register/',views.flat_register,name='flat-register'),
	path('flat-dashboard/',views.flat_dashboard,name='flat-dashboard'),
	path('flat-forgotpass1/',views.flat_forgotpass1,name='flat-forgotpass1'),
	path('flat-forgotpass2/',views.flat_forgotpass2,name='flat-forgotpass2'),
	path('flat-forgotpass3/',views.flat_forgotpass3,name='flat-forgotpass3'),
]
