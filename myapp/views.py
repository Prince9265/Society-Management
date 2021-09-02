from django.shortcuts import render,HttpResponse
from django.http import request
from django.conf import settings
from django.core.mail import send_mail
from random import randrange
from .models import *

def login(request):
	if request.method=="POST":
		email=request.POST['email']
		

		password=request.POST['password']

		try:
			uid = User.objects.get(email=request.POST['email'])
		except:
			msg="Email is not registered"
			return render(request,'login.html',{'msg':msg})

		if password == uid.password:
			request.session['email']=request.POST['email']
			return render(request,'dashboard.html',{'uid':uid})
		else:
			msg='password does not match'
			return render(request,'login.html',{'msg':msg})
	else:
		return render(request,'login.html')

def logout(request):
	del request.session['email']
	return render(request,'login.html')

def index(request):
	uid=User.objects.get(email=request.session['email'])
	return render(request,'dashboard.html',{'uid':uid})

def profile(request):
	uid=User.objects.get(email=request.session['email'])
	if request.method=='POST':
		uid.mobile=request.POST['mobile']
		uid.name=request.POST['name']
		uid.password=request.POST['password']
		if 'pic' in request.FILES:
			uid.pic=request.FILES['pic']
		uid.save()
	return render(request,'profile.html',{'uid':uid})

def register(request):
	if request.method=='POST':
		name=request.POST['name']
		mobile=request.POST['mobile']
		email=request.POST['email']
		password=request.POST['password']
		cpassword=request.POST['cpassword']

		if password==cpassword:
			global temp
			temp = {
				'name' : name,
				'email' : email,
				'mobile' : mobile,
				"password" : password,
			}
			otp = randrange(1000,9999)
			subject = 'Welcome to Society Management'
			message = f'Hi, your otp is {otp} Thank you for registering.'
			email_from = settings.EMAIL_HOST_USER
			recipient_list = [email, ]
			send_mail( subject, message, email_from, recipient_list )
			return render(request,'otp.html',{'otp':otp})
		else:
			msg='Password and Confirm password does not Match'
			return render(request,"register.html",{'msg':msg})

	else:
		return render(request,'register.html')

def otp(request):
	if request.method == "POST":
		otp=request.POST['otp']
		uotp=request.POST['uotp']

		if otp == uotp:
			User.objects.create(
            	name = temp['name'],
                mobile = temp['mobile'],
                email = temp['email'],
                password = temp['password'],
                )
			return render(request,'login.html')
		else:
			msg = 'OTP does not matched'
			return render(request,'otp.html',{'otp':otp,'msg':msg})

	else:
		return render(request,'otp.html')

def forgot_pass1(request):
	if request.method=='POST':
		email=request.POST['email']
		try:
			uid=User.objects.get(email=email)
		except:
			msg='Email does not exist'
			return render(request,'forgot pass1.html',{'msg':msg})
		otp = randrange(1000,9999)
		subject = 'Welcome to Society Management'
		message = f'Hi your otp for Reset password is {otp}.'
		email_from = settings.EMAIL_HOST_USER
		recipient_list = [email, ]
		send_mail( subject, message, email_from, recipient_list )
		return render(request,'forgot pass2.html',{'otp':otp,'email':email})
	else:
		return render(request,'forgot pass1.html')

def forgot_pass2(request):
	if request.method=='POST':
		otp=request.POST['otp']
		uotp=request.POST['uotp']
		email=request.POST['email']
		if otp==uotp:
			return render(request,'forgot pass3.html',{'email':email})
		else:
			msg='OTP does not matched'
			return render(request,'forgot pass2.html',{'email':email,'msg':msg,'otp':otp})
	else:
		return render(request,'forgot pass2.html')

def forgot_pass3(request):
	if request.method=='POST':
		email=request.POST['email']
		password=request.POST['password']
		cpassword=request.POST['cpassword']
		if password==cpassword:
			uid=User.objects.get(email=email)
			uid.password=password
			uid.save()
			return render(request,'login.html')
		else:
			msg='Password and Confirm Password does not Match'
			return render(request,"forgot pass3.html",{'email':email,'msg':msg})
	else:
		return render(request,"forgot pass3.html")

def table(request):
	return render(request,'table.html')

def add_event(request):
	uid=User.objects.get(email=request.session['email'])
	if request.method == 'POST':
		if 'epic' in request.FILES:
			Event.objects.create(
				uid=uid,
				etitle=request.POST['etitle'],
				edate=request.POST['edate'],
				edis=request.POST['edis'],
				epic=request.FILES['epic'],
				)
		else:
			Event.objects.create(
				uid=uid,
				etitle=request.POST['etitle'],
				edate=request.POST['edate'],
				edis=request.POST['edis'],
				)
		msg='Event Created'
		return render(request,'add-event.html',{'uid':uid,'msg':msg})

	else:
		return render(request,'add-event.html',{'uid':uid})

def all_event(request):
	uid=User.objects.get(email=request.session['email'])
	events=Event.objects.all()[::-1]
	return render(request,'all-event.html',{'events':events,'uid':uid})

def edit_event(request,pk):
	uid=User.objects.get(email=request.session['email'])
	eid=Event.objects.get(id=pk)
	edate=str(eid.edate)
	if request.method=='POST':
		eid.etitle=request.POST['etitle']
		eid.edate=request.POST['edate']
		eid.edis=request.POST['edis']
		if 'epic' in request.FILES:
			eid.epic=request.FILES['epic']
		eid.save()
		events=Event.objects.all()
		return render(request,'all-event.html',{'events':events,'uid':uid})
	else:
		return render(request,'edit-event.html',{'eid':eid,'uid':uid,'edate':edate})

def delete_event(request,pk):
	uid=User.objects.get(email=request.session['email'])
	eid= Event.objects.get(id=pk)
	eid.delete()
	events=Event.objects.all()
	return render(request,'all-event.html',{'uid':uid,'events':events})

def add_member(request):
	return render(request,'add-member.html')