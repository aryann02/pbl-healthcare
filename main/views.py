# views.py

from django.shortcuts import render, redirect
from .models import Doctor, Appointment
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages

# @login_required
def landing_page(request):
    if request.method == 'POST':
        location = request.POST.get('location')
        doctors = Doctor.objects.filter(location__icontains=location)
        return render(request, 'main/landing_page.html', {'doctors': doctors})
    
    return render(request, 'main/landing_page.html')


from django.utils.dateparse import parse_date, parse_time

@login_required()   # login page rediret
def book_appointment(request, doctor_id):
    doctor = Doctor.objects.get(id=doctor_id)
    
    if request.method == 'POST':
        date = request.POST.get('date')
        time = request.POST.get('time')

        if not date or not time:
            messages.error(request, "Please select both a date and time for the appointment.")
            return render(request, 'main/book_appointment.html', {'doctor': doctor})
        
        try:
            appointment_date = parse_date(date)
            appointment_time = parse_time(time)
            
            if appointment_date and appointment_time:
                Appointment.objects.create(
                    user=request.user,
                    doctor=doctor,
                    date=appointment_date,
                    time=appointment_time
                )
                messages.success(request, 'Appointment booked successfully!')
                return redirect('success')
            else:
                messages.error(request, "Invalid date or time selected.")
        except ValueError:
            messages.error(request, "An error occurred while processing the date or time.")
    
    return render(request, 'main/book_appointment.html', {'doctor': doctor})

def index(request):
        return render(request, 'main/index.html', {'doctor': "doctor"})
    
def success(request):
        return render(request, 'main/appointment_success.html', {'doctor': "doctor"})
    



from main.forms import *
from main.models import *
from django.contrib import messages


def User_Register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST , request=request)
        try:
            if form.is_valid():
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password']) 
                user.save()
                messages.success(request, 'Registration successful! Please login.')

                return redirect('register') 
        except Exception as e:
            messages.warning(request,'An error occurred during register. Please try again.')
            return redirect('register')
    else:
        form = UserRegistrationForm(request=request)
    return render(request, 'main/signup.html', {'form': form})



from django.contrib.auth import authenticate, logout ,login 
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST , request=request)
        try:
            if form.is_valid():
               # import pdb;pdb.set_trace();
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')

                if not username or not password:
                    add_message(request,'warning', 'Username and Password are required.')
                    return redirect('login')

                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('index')
                else:
                    add_message(request,'warning', 'Invalid Username or Password.')
                    return redirect('login')
        except Exception as e:
            add_message(request, 'warning','An error occurred during login. Please try again.')
            return redirect('login')

    else:
        form =LoginForm(request=request)
        return render(request, 'main/login.html', {'form': form})


