from django.urls import path
from main.views import *
from django.contrib import admin

urlpatterns = [
    path('admin/' , admin.site.urls),
    path('find_doctor/', landing_page, name='find_doctor'),
    path('book_appointment/<int:doctor_id>/', book_appointment, name='book_appointment'),
    path('', index, name='index'),
    path('register/', User_Register, name='register'),
    path('success/', success, name='success'),
    path('login/', user_login, name='login'),
]



