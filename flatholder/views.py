from django.shortcuts import render,HttpResponse
from django.http import request
from django.conf import settings
from django.core.mail import send_mail
from random import randrange

import myapp
from .models import *
from myapp import models

# Create your views here.
def flat_login(request):
	if request.method=='POST':
		try:
			uid=Userf.objects.get(email=request.POST['email'])
			if uid.password == request.POST['password']:
				request.session['femail']=request.POST['email']
				events=models.Event.objects.all()[::-1]
				return render(request,'flat-dashboard.html',{'uid':uid,'events':events})
			else:
				msg='Password does not Match'
				return render(request,'flat-login.html',{'msg':msg})
		except:
			msg='User is not registered'
			return render(request,'flat-login.html',{'msg':msg})
	else:
		return render(request,'flat-login.html')

def flat_register(request):
	if request.method=='POST':
		try:
			uid=Userf.objects.get(email=request.POST['email'])
			msg="Email is already Register"
			return render(request,'flat-register.html',{'msg':msg})
		except:
			if request.POST['password']==request.POST['cpassword']:
				Userf.objects.create(
					fname=request.POST['fname'],
					lname=request.POST['lname'],
					birth=request.POST['birth'],
					email=request.POST['email'],
					mobile=request.POST['mobile'],
					password=request.POST['password'],
					address=request.POST['address'],
					occupation=request.POST['occupation'],
					
				)
				msg='User Created'
				return render(request,'flat-register.html',{'msg':msg})
			else:
				msg='Password and Confirm Password does not Match'
				return render(request,'flat-register.html',{'msg':msg})
	else:
		return render(request,'flat-register.html')

def flat_logout(request):
	del request.session['femail']
	return render(request,'flat-login.html')

def flat_dashboard(request):
	return render(request,'dashboard.html')

def flat_forgotpass1(request):
	if request.method=='POST':
		email=request.POST['email']
		try:
			uid=Userf.objects.get(email=email)
		except:
			msg="Email does not exist"
			return render(request,'flat-forgotpass1.html',{'msg':msg})

		otp = randrange(1000,9999)
		subject = 'Welcome to Society Management'
		message = f'Hi your otp for Reset password is {otp}.'
		email_from = settings.EMAIL_HOST_USER
		recipient_list = [email, ]
		send_mail( subject, message, email_from, recipient_list )
		return render(request,'flat-forgotpass2.html',{'otp':otp,'email':email})
	else:
		return render(request,'flat-forgotpass1.html')

def flat_forgotpass2(request):
	if request.method=='POST':
		email=request.POST['email']
		otp=request.POST['otp']
		uotp=request.POST['uotp']
		if otp==uotp:
			return render(request,'flat-forgotpass3.html',{'email':email})
		else:
			msg="OTP does not match"
			return render(request,'flat-forgotpass2.html',{'email':email,'otp':otp,'msg':msg})
	else:
		return render(request,'flat-forgotpass2.html')

def flat_forgotpass3(request):
	if request.method=='POST':
		email=request.POST['email']
		password=request.POST['password']
		cpassword=request.POST['cpassword']
		if password==cpassword:
			uid=Userf.objects.get(email=email)
			uid.password=password
			uid.save()
			return render(request,'flat-login.html')
		else:
			msg='Password and Confirm Password does not Match'
			return render(request,'flat-forgotpass3.html',{'email':email,'msg':msg})
	else:
		return render(request,'flat-forgotpass3.html')