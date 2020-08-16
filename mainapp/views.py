from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import Submit,Classes,MutualTable
from django.utils.crypto import get_random_string


# Create your views here.
def home(request):
    return render(request,'home.html')


def newClass(request):
	if request.method == 'POST':
		user = request.user
		name = user.username
		clsCode = get_random_string(length=32)
		if Classes.objects.filter(clsCode=clsCode).exists():
			while Classes.objects.filter(clsCode=clsCode).exists():
				clsCode = get_random_string(length=32)

		cls_name = request.POST['cls_name']
		if user.is_authenticated :
			if Classes.objects.filter(cls_name=cls_name,ownedby=user.username).exists():
				messages.info(request,'You already have used same name for a class!')
				return redirect('newClass')
			else:
				x = Classes(cls_name=cls_name,ownedby=name,clsCode=clsCode, )
				x.save()
				obj = MutualTable(cls_name=cls_name,ownedby=name,is_active=True)
				obj.save()
				messages.info(request,'Classes is created, share the security code '+ x.clsCode+' with students now!')
				return redirect('teacherPage')
	else:
		return render(request,'newClass.html')



def studentPage(request):
	if request.method == 'POST':
		clsCode = request.POST['clsCode']
		stu_id = request.POST['stu_id']
		if clsCode=="" or stu_id=="":
			return redirect('studentPage')
		xs = Classes.objects.filter(clsCode__contains=clsCode)
		c=xs.count()
		if c>0:
			ownedby = xs[0].ownedby
			cls_name = xs[0].cls_name
			y = MutualTable.objects.get(cls_name=cls_name,ownedby=ownedby)
			if y.is_active == True:
				obj = Submit(stu_id=stu_id,cls_name=cls_name,ownedby=ownedby)
				obj.save()
				messages.info(request,'Attendance Submitted')
				return redirect('studentPage')
			else:
				messages.info(request,'Sorry, class code is not valid!')
				return redirect('studentPage')
		else:
			messages.info(request,'Invalid Class Code')
			return redirect('studentPage')
	else:
		return render(request,'studentPage.html')


def login(request):
	if request.method== 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user= auth.authenticate(username=username,password=password)
		if user is not None:
			auth.login(request, user)
			return redirect('teacherPage')
		else:
			messages.info(request,'Wrong Password or User name!')
			return redirect('login')

	else:
		u =request.user
		if u.is_authenticated:
			return redirect('teacherPage')
		else:
			return render(request,'login.html')

def logout(request):
	auth.logout(request)
	return redirect('/')


def register(request):
	if request.method == 'POST' :
		first_name=request.POST['fname']
		last_name=request.POST['lname']
		username=request.POST['username']
		email=request.POST['email']
		password1=request.POST['password1']
		password2=request.POST['password2']

		if password1==password2 :
			if User.objects.filter(username=username).exists():
				messages.info(request,'User Name Taken')
				return redirect('register')
			elif User.objects.filter(email=email).exists():
				messages.info(request,'Email Taken')
				return redirect('register')
			else:	
			    user = User.objects.create_user(username=username,password=password1,email=email,first_name=first_name,last_name=last_name)
			    user.save();
			    return redirect('login')
		else:
		 	messages.info(request,'Password did not match')
		 	return redirect('register')
		return redirect('/')
	else:
		return render(request,"register.html")


def classList(request):
	user = request.user
	name = user.username
	if user.is_authenticated:
		y = MutualTable.objects.filter(ownedby=name)
		return render(request,"classList.html",{"classes":y})


def teacherPage(request):
	user = request.user
	if user.is_authenticated:
		return render(request,'teacherPage.html')
	else:
		return redirect('login')


def classrecord(request,classname):
	user = request.user
	if user.is_authenticated:
		x = Classes.objects.filter(cls_name=classname,ownedby=user.username)
		active = MutualTable.objects.filter(cls_name=classname,ownedby=user.username)
		y = x[0].cls_name
		z = Submit.objects.filter(cls_name=y,ownedby=user.username)
		return render(request,"show.html",{"student":z,"cls_name":classname,"k":x[0].clsCode})
	else:
		return redirect('login')


def turnoff(request,classname):
	user = request.user
	if user.is_authenticated:
		x=MutualTable.objects.get(ownedby=user.username,cls_name=classname)
		if x.is_active == True:
			x.is_active = False
			x.save()
			return redirect('classList')
		else:
			x.is_active=True
			x.save()
			return redirect('classList')
	else:
		return redirect('login')


def generate(request,classname):
	clsCode = get_random_string(length=32)
	while Classes.objects.filter(clsCode=clsCode).exists():
		clsCode = get_random_string(length=32)
	user = request.user
	username = user.username
	if not user.is_authenticated:
		return redirect('login')
	else:
		if request.method == 'POST':
			x = Classes.objects.get(cls_name=classname,ownedby=username)
			x.clsCode=clsCode
			x.save()
			messages.info(request,'New key generated')
			return redirect('classList')

def delete(request,classname):
	user = request.user
	if user.is_authenticated:
		ownedby = user.username
		x = Classes.objects.get(cls_name=classname,ownedby=ownedby)
		x.delete()
		y = MutualTable.objects.get(cls_name=classname,ownedby=ownedby)
		y.delete()
		return redirect('classList')
	else:
		return redirect('login')

