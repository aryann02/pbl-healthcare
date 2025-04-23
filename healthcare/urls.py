from django.urls import path
from main.views import *
# from main.views import update_appointment_status
from django.contrib import admin

urlpatterns = [
    path('admin/' , admin.site.urls),\
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', user_register, name='register'),


    path('', index, name='index'),  # homepage
    path('doctor/', doctor_list, name='doctor'), #doctor_list
    path('book_appointment/<int:doctor_id>/', book_appointment, name='book_appointment'), # appointment
    path('success/', appointment_success, name='success'), # success
    path('doctor_dashboard/', doctor_dashboard, name='doctor_dashboard'), # doctor_dashboard
    path('add_doctor/', add_doctor, name='add_doctor'), # doctor_dashboard
]



