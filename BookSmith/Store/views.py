from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import *
from .forms import CreateUser, AddBook

# Create your views here.

# references :
# https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html

def index(request):
	return HttpResponse('<b>INDEX PAGE</b>')


def register(request):
	if request.method == "POST":
		# print(request.POST)
		
		form = CreateUser(request.POST)
		print(type(form))
		for key in form:
			print(key, ": ", key.errors)
		# instance = form.save()
		if form.is_valid():
			print("FORM IS VALID")
			
			# Saving details of new user
			# I tried doing form.save() but it wasn't hashing password

			instance = User.objects.create_user(**form.cleaned_data)
			
			print(instance.__dict__)
			# Linking to vendor or customer model
			is_vendor = instance.is_vendor
			if is_vendor:
				new_vendor = Vendor()
				new_vendor.vendor_details = instance
				new_vendor.save()
			else:
				new_customer = Customer()
				new_customer.customer_details = instance
				new_customer.save()
			return HttpResponse("<b>User Created Successfully</b>")
		else:
			print("Form is invalid")
			context = {
			"form" : form,
			}
			return render(request, 'Store/register.html', context)
	else:
		form = CreateUser()
		context = {
		"form" : form,
		}
		return render(request, 'Store/register.html', context)


def log_in(request):
	if request.method == "POST":
		username = request.POST["username"]
		password = request.POST["password"]
		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			# return HttpResponse(f"<b>{user.username} logged in </b>")
			if user.is_vendor:
				# vendor = user.vendor_set.first()
				# books = vendor.book_set.all()
				# context = {
				# 	"books" : books,
				# }
				# return render(request, 'Store/index_vendor.html', context=context)
				return HttpResponseRedirect(reverse('index-vendor'))
			else:
				# books = Book.objects.all()
				# context = {
				# 	"books" : books,
				# }
				# return render(request, 'Store/index_customer.html', context)
				return HttpResponseRedirect(reverse('index-customer'))
		
		else:
			context = {
				"message" : "Invalid username and/or password",
			}

			return render(request, 'Store/login.html', context)
		pass
	else:
		return render(request, "Store/login.html")


@login_required
def log_out(request):
	logout(request)
	return HttpResponseRedirect(reverse('index'))

@login_required
def index_customer(request):
	user = request.user
	if user.is_vendor:
		return HttpResponseRedirect(reverse('index-vendor'))
	books = Book.objects.all()
	context = {
		"books" : books,
	}
	return render(request, 'Store/index_customer.html', context)

@login_required
def index_vendor(request):
	user = request.user
	if not user.is_vendor:
		return HttpResponseRedirect(reverse('index-customer'))

	vendor = user.vendor_set.first()
	books = vendor.book_set.all()
	context = {
		"books" : books,
	}
	return render(request, 'Store/index_vendor.html', context=context)

@login_required
def addbook(request):
	if request.method == "POST":
		print("Request : ", request.POST)
		form = AddBook(request.POST, request.FILES)
		try:
			if form.is_valid():
				print("Form Validated")

				# Don't commit because we need to assign vendor, category
				# Also we need to change the name of image uploaded
				instance = form.save(commit=False)
				print("Instance commit False : ", instance)
				category_name = request.POST.get('category')

				# If category exists already
				obj = Category.objects.filter(category=category_name).first()

				# If doesn't exist, create one
				if obj is None:
					obj = Category(category=category_name)
					obj.save()

				# Assign category to instance
				instance.category = obj

				# Logged in user is a part of User class, to get the corresponding vendor :
				vendor = request.user.vendor_set.first()
				instance.vendor = vendor

				instance.save()
				return HttpResponse("<b>Valid Form and Book Added!</b>")

			else:
				form = AddBook(request.POST, request.FILES)
				context = {
					"form" : form,
					"message" : "Inavlid Input. Please Fill All Details Correctly."
				}
				return render(request, 'Store/addbook.html', context)
		except Exception as e:
			context = {
				"form" : form,
				"message" : "Some Error Occurred. Try Again."
			}
			print(f"Exception {e} Occurred.")
			return render(request, 'Store/addbook.html', context)

	else:
		form = AddBook()
		context = {
		"form" : form,
		}
		return render(request, 'Store/addbook.html', context)