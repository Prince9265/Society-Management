from django.shortcuts import render,HttpResponse
from django.http import request
from django.conf import settings
from django.core.mail import send_mail
from random import randrange
from django.http.response import JsonResponse

import myapp
from .models import *
from myapp import models
from .paytm import generate_checksum, verify_checksum
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def flat_index(request):
	return render(request,'flat-index.html')

def flat_login(request):
	if 'femail' in request.session:
		uid=Userf.objects.get(email=request.session['femail'])
		return render(request,'flat-dashboard.html',{'uid':uid})
	else:
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

# def flat_register(request):
# 	if request.method=='POST':
# 		try:
# 			uid=Userf.objects.get(email=request.POST['email'])
# 			msg="Email is already Register"
# 			return render(request,'flat-register.html',{'msg':msg})
# 		except:
# 			if request.POST['password']==request.POST['cpassword']:
# 				Userf.objects.create(
# 					fname=request.POST['fname'],
# 					lname=request.POST['lname'],
# 					birth=request.POST['birth'],
# 					email=request.POST['email'],
# 					mobile=request.POST['mobile'],
# 					password=request.POST['password'],
# 					address=request.POST['address'],
# 					occupation=request.POST['occupation'],	
# 				)
# 				msg='User Created'
# 				return render(request,'flat-register.html',{'msg':msg})
# 			else:
# 				msg='Password and Confirm Password does not Match'
# 				return render(request,'flat-register.html',{'msg':msg})
# 	else:
# 		return render(request,'flat-register.html')

def flat_register(request):
	if request.method=='POST':
		fname=request.POST['fname']
		lname=request.POST['lname']
		birth=request.POST['birth']
		email=request.POST['email']
		mobile=request.POST['mobile']
		password=request.POST['password']
		cpassword=request.POST['cpassword']
		address=request.POST['address']
		occupation=request.POST['occupation']
		try:
			uid=Userf.objects.get(email=email)
			msg='Email Already Exist'
			return render(request,'flat-login.html',{"msg":msg})
		except:
			if password == cpassword:
				if len(password) >= 8:

					global temp
					temp={
						'fname':fname,
						'lname':lname,
						'birth':birth,
						'email':email,
						'mobile':mobile,
						'password':password,
						'address':address,
						'occupation':occupation,
					}
					otp = randrange(1000,9999)
					subject = 'welcome to Society Management'
					message = f'Hi your otp is {otp} , thank you for registering.'
					email_from = settings.EMAIL_HOST_USER
					recipient_list = [email, ]
					send_mail( subject, message, email_from, recipient_list )
					return render(request,'flat-otp.html',{'otp':otp})
				else:
					msg1 = 'your password must be at least 8 characters'
					return render(request,'flat-register.html',{'msg1':msg1})
			else:
				msg = 'Password and Confirm password does not matched'
				return render(request,'flat-register.html',{'msg':msg})
	else:
		return render(request,'flat-register.html')


def flat_otp(request):
	if request.method=='POST':
		otp=request.POST['otp']
		uotp=request.POST['uotp']
		if otp == uotp:
			Userf.objects.create(
					fname=temp['fname'],
					lname=temp['lname'],
					birth=temp['birth'],
					email=temp['email'],
					mobile=temp['mobile'],
					password=temp['password'],
					address=temp['address'],
					occupation=temp['occupation'],	
				)
			return render(request,'flat-login.html')
		else:
			msg='OTP does not match'
			return render(request,'flat-otp.html',{'msg':msg,'otp':otp})

	else:
		return render(request,'flat-otp.html')


def flat_logout(request):
	del request.session['femail']
	return render(request,'flat-index.html')

def flat_dashboard(request):
	uid= Userf.objects.get(email=request.session['femail'])
	return render(request,'flat-dashboard.html',{'uid':uid})

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

def flat_profile(request):
	uid=Userf.objects.get(email=request.session['femail'])
	ubirth=str(uid.birth)
	if request.method == 'POST':
		uid.fname=request.POST['fname']
		uid.lname=request.POST['lname']
		uid.birth=request.POST['birth']
		uid.mobile=request.POST['mobile']
		uid.address=request.POST['address']
		uid.birth=request.POST['birth']
		uid.occupation=request.POST['occupation']
		uid.password=request.POST['password']
		if 'pic' in request.FILES:
			uid.pic=request.FILES['pic']
		uid.save()
		# flat=(
		# 	fname=request.POST['fname']
		# 	lname=request.POST['lname']
		# 	birth=request.POST['birth']
		# 	mobile=request.POST['mobile']
		# 	address=request.POST['address']
		# 	birth=request.POST['birth']
		# 	occupation=request.POST['occupation']
		# 	password=request.POST['password']
		# 	pic=request.FILES['pic']
		# 	)
		# profile=list(Userf.objects.values())
		# return JsonResponse({'uid':uid,'ubirth':ubirth,'profile':profile})
		return render(request,'flat-profile.html',{'uid':uid,'ubirth':ubirth})
	else:
		uid=Userf.objects.get(email=request.session['femail'])
		return render(request,"flat-profile.html",{'uid':uid,'ubirth':ubirth})

	
def flat_table(request):
	return render(request,'flat-table.html')

def flat_complain(request):
	uid=Userf.objects.get(email=request.session['femail'])
	if request.method=='POST':
		if 'cpic' in request.FILES:
			Complain.objects.create(
				uid=uid,
				title=request.POST['ctitle'],
				dis=request.POST['cdis'],
				place=request.POST['cplace'],
				cpic=request.FILES['cpic'],
				)
		else:
			Complain.objects.create(
				uid=uid,
				title=request.POST['ctitle'],
				dis=request.POST['cdis'],
				place=request.POST['cplace'],
				)
		msg="Complain Added"
		return render(request,'flat-complain.html',{'uid':uid,'msg':msg})
	else:
		return render(request,'flat-complain.html',{'uid':uid})

def flat_mycomplain(request):
	uid=Userf.objects.get(email=request.session['femail'])
	complains=Complain.objects.all()[::-1]
	return render(request,'flat-mycomplain.html',{'complains':complains,'uid':uid})

def flat_event(request):
	uid=Userf.objects.get(email=request.session['femail'])
	events=models.Event.objects.all()[::-1]
	return render(request,'flat-event.html',{'events':events,"uid":uid})

def flat_rentbuyhouse(request):
	uid=Userf.objects.get(email=request.session['femail'])
	if request.method=="POST":
		if 'rbpic' in request.FILES:
			RentBuyHouse.objects.create(
				uid=uid,
				type1=request.POST['rbtype'],
				rbprice=request.POST['rbprice'],
				rbpic=request.FILES['rbpic'],
				)
		else:
			RentBuyHouse.objects.create(
				uid=uid,
				type1=request.POST['rbtype'],
				rbprice=request.POST['rbprice'],
				)
		msg='Successfully Added'
		showhouse=RentBuyHouse.objects.all()[::-1]
		return render(request,'flat-rentbuyhouse.html',{'uid':uid,'msg':msg,'showhouse':showhouse})
	else:
		showhouse=RentBuyHouse.objects.all()[::-1]
		return render(request,'flat-rentbuyhouse.html',{'uid':uid,'showhouse':showhouse})

def flat_showrentbuyhouse(request):
	uid=Userf.objects.get(email=request.session['femail'])
	showhouse=RentBuyHouse.objects.all()[::-1]
	return render(request,'flat-rentbuyhouse.html',{'uid':uid,'showhouse':showhouse})

def flat_contact(request,pk):
	uid=Userf.objects.get(email=request.session['femail'])
	contact_id=RentBuyHouse.objects.get(id=pk)
	email=contact_id.uid.email
	subject = 'Welcome to Society Management'
	message = f'Hi, {uid.fname} {uid.lname} is Intrested to your {contact_id.type1} \n  Instrusted Person Details: \n \t email:{uid.email} \n \t Mobile Number:{uid.mobile} \n \n Thank you for visiting.'
	email_from = settings.EMAIL_HOST_USER
	recipient_list = [email, ]
	send_mail( subject, message, email_from, recipient_list )
	showhouse=RentBuyHouse.objects.all()[::-1]
	return render(request,'flat-rentbuyhouse.html',{'uid':uid,'showhouse':showhouse})

def flat_search(request):

	search=request.POST['fsearch']
	users=Userf.objects.all()
	return render(request,'flat-search.html',{'search':search,'users':users})

def flat_pay(request):
	return render(request,'pay.html',{'uid':uid})



def initiate_payment(request):
    if request.method == "GET":
    	uid = Userf.objects.get(email=request.session['femail'])
    	return render(request, 'pay.html',{'uid':uid})
    try:
        amount = int(request.POST['amount'])
        year = request.POST['year']
        month = request.POST['month']
        uid=Userf.objects.get(email=request.session['femail'])

    except:
        return render(request, 'pay.html', context={'error': 'Wrong Accound Details or amount'})

    transaction = Transaction.objects.create(made_by=uid,month=month,year=year, amount=amount)
    transaction.save()
    merchant_key = settings.PAYTM_SECRET_KEY

    params = (
        ('MID', settings.PAYTM_MERCHANT_ID),
        ('ORDER_ID', str(transaction.order_id)),
        ('CUST_ID', str(transaction.made_by.email)),
        ('TXN_AMOUNT', str(transaction.amount)),
        ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
        ('WEBSITE', settings.PAYTM_WEBSITE),
        # ('EMAIL', request.user.email),
        # ('MOBILE_N0', '9911223388'),
        ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
        ('CALLBACK_URL', 'http://127.0.0.1:8000/callback/'),
        # ('PAYMENT_MODE_ONLY', 'NO'),
    )

    paytm_params = dict(params)
    checksum = generate_checksum(paytm_params, merchant_key)

    transaction.checksum = checksum
    transaction.save()

    paytm_params['CHECKSUMHASH'] = checksum
    print('SENT: ', checksum)
    return render(request, 'redirect.html', context=paytm_params)


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        received_data = dict(request.POST)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            received_data['message'] = "Checksum Matched"
        else:
            received_data['message'] = "Checksum Mismatched"
            return render(request, 'callback.html', context=received_data)
        return render(request, 'callback.html', context=received_data)

def maintanance(request):
	details=Transaction.objects.all()[::-1]
	uid=Userf.objects.get(email=request.session['femail'])
	return render(request,'maintanance.html',{'details':details,'uid':uid})














