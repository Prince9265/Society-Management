from django.contrib import admin
from django.http import request
from django.urls import path
from . import views

urlpatterns = [
	path('',views.flat_index,name='flat-index'),
	path('flat-login',views.flat_login,name='flat-login'),
	path('flat-register/',views.flat_register,name='flat-register'),
	path('flat-dashboard/',views.flat_dashboard,name='flat-dashboard'),
	path('flat-forgotpass1/',views.flat_forgotpass1,name='flat-forgotpass1'),
	path('flat-forgotpass2/',views.flat_forgotpass2,name='flat-forgotpass2'),
	path('flat-forgotpass3/',views.flat_forgotpass3,name='flat-forgotpass3'),
	path('flat-logout/',views.flat_logout,name='flat-logout'),
	path('flat-profile/',views.flat_profile,name='flat-profile'),
	path('flat-table/',views.flat_table,name='flat-table'),
	path('flat-complain/',views.flat_complain,name='flat-complain'),
	path('flat-mycomplain/',views.flat_mycomplain,name='flat-mycomplain'),
	path('flat-otp/',views.flat_otp,name='flat-otp'),
	path('flat-rentbuyhouse',views.flat_rentbuyhouse,name='flat-rentbuyhouse'),
	path('flat-event/',views.flat_event,name='flat-event'),
	path('flat-contact/<int:pk>',views.flat_contact,name='flat-contact'),
	path('flat-search/',views.flat_search,name='flat-search'),
	path('flat-pay/',views.initiate_payment,name='flat-pay'),
	path('callback/', views.callback, name='callback'),
	path('maintanance/',views.maintanance,name='maintanance'),

]
