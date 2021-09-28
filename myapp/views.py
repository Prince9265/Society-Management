from django.shortcuts import render,HttpResponse
from django.http import request
from django.conf import settings
from django.core.mail import send_mail
from random import randrange
from .models import *
from random import randrange,choices

from django.shortcuts import render
from django.http.response import JsonResponse
from flatholder import models 

def login(request):
	if 'email' in request.session:
		uid=User.objects.get(email=request.session['email'])
		return render(request,'dashboard.html',{'uid':uid})
	else:
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


# def profile(request):
# 	if request.method=='POST':
# 		uid=User.objects.get(email=request.session['email'])
		
# 		uid.mobile=request.POST['mobile'],
# 		uid.name=request.POST['name'],
# 		uid.password=request.POST['password'],
# 		if 'pic' in request.FILES:
# 			uid.pic=request.FILES['pic'],
# 		uid.save()
		
		
# 		return JsonResponse({'abc':'Updated'})
# 	else:
# 		uid=User.objects.get(email=request.session['email'])
		
# 		return render(request,'profile.html',{'uid':uid})



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
	if request.method == 'POST':
		try:
			uid = models.Userf.objects.get(email=request.POST['email'])
			msg = 'Already Exist'
			return render(request,'add-member.html',{'msg':msg,'uid':uid})
		except:
			s = 'abcdefghijklmn123654789ABCDEFGHIJK'
			password = ''.join(choices(s,k=8))
			subject = 'New User Created'
			message = f"Hey, Your account is created and password is : {password}"
			email_from = settings.EMAIL_HOST_USER
			recipient_list = [request.POST['email'],]
			send_mail( subject, message, email_from, recipient_list )
			if 'pic' in request.FILES:
				models.Userf.objects.create(
				    fname = request.POST['fname'],
				    lname = request.POST['lname'],
				    email = request.POST['email'],
				    mobile = request.POST['mobile'],
				    password = password,
				    birth = request.POST['birth'],
				    address = request.POST['address'],
				    occupation = request.POST['occupation'],
				    pic = request.FILES['pic'],
				)
			else:
				models.Userf.objects.create(
					fname = request.POST['fname'],
				    lname = request.POST['lname'],
				    email = request.POST['email'],
				    mobile = request.POST['mobile'],
				    password = password,
				    birth = request.POST['birth'],
				    address = request.POST['address'],
				    occupation = request.POST['occupation'],   
				)
				msg='User Created'
				return render(request,'add-member.html',{'msg':msg})
	else:
		return render(request,'add-member.html')


def all_member(request):
	users = models.Userf.objects.all()
	return render(request,'all-member.html',{'users':users})

def flat_role(request,pk):
	role_id=models.Userf.objects.get(id=pk)
	users = models.Userf.objects.all()
	if role_id.role == 'user':
		role_id.role = 'member'
		role_id.save()
		return render(request,'all-member.html',{'users':users})
	else:
		role_id.role = 'user'
		role_id.save()
		return render(request,'all-member.html',{'users':users})

def view_complain(request):
	complains=models.Complain.objects.all()
	return render(request,'view-complain.html',{'complains':complains})

def complain_status(request,pk):
	complains=models.Complain.objects.all()
	complain_id=models.Complain.objects.get(id=pk)
	complain_id.status = 'CLOSE'
	complain_id.save()
	return render(request,'view-complain.html',{'complains':complains})

def all_complain(request):
	complains=models.Complain.objects.all()[::-1]
	return render(request,'all-complain.html',{'complains':complains})

def sec_maintanance(request):
	details=models.Transaction.objects.all()
	return render(request,'sec-maintanance.html',{'details':details})