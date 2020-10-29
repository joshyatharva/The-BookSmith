from django.urls import path
from . import views



urlpatterns = [

	path('', views.index, name='index'),
	path('register', views.register, name='register'),
	path('login', views.log_in, name='login'),
	path('logout', views.log_out, name='logout'),
	path('vendor/addbook', views.addbook, name='addbook'),
	path('vendor/index', views.index_vendor, name='index-vendor'), 
	path('customer/index', views.index_customer, name='index-customer'),
]

