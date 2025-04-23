from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.utils.dateparse import parse_date, parse_time
from datetime import datetime, timedelta, date

from .models import Doctor, Appointment
from .forms import UserRegistrationForm, LoginForm


# --------------------- Utility ---------------------

def generate_time_slots(start, end, interval_minutes=30):
    slots = []
    current = datetime.combine(datetime.today(), start)
    end_time = datetime.combine(datetime.today(), end)
    while current < end_time:
        slots.append(current.strftime('%H:%M'))
        current += timedelta(minutes=interval_minutes)
    return slots


# --------------------- Public Views ---------------------

def landing_page(request):
    return render(request, 'main/landing_page.html')


def index(request):
    return render(request, 'main/index.html')


from django.shortcuts import render
from .models import Appointment

def appointment_success(request, appointment_id):
    # Retrieve the appointment object by ID
    appointment = Appointment.objects.get(id=appointment_id)
    
    # Pass the appointment data to the template
    return render(request, 'main/appointment_success.html', {'appointment': appointment})



def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request, 'main/doctor.html', {'doctors': doctors})


# --------------------- Authentication Views ---------------------

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm

def user_register(request):
    # import pdb;pdb.set_trace()
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request=request)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Set the password securely
            user.save()
            messages.success(request, 'Registration successful! Please login.')
            return redirect('login')
        else:
            messages.error(request, 'Invalid data. Please correct the errors below.')
    else:
        form = UserRegistrationForm(request=request)

    return render(request, 'main/signup.html', {'form': form})



def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST, request=request)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                if user.role == 'DOCTOR':
                        #return redirect('homepage')
                        return redirect('index')
                        #return HttpResponse("<h1>Welcome To Buyer page.</h1>")   
                if user.role == 'PATIENT':
                        return redirect('index')
                return redirect('index')
            else:
                messages.warning(request, 'Invalid Username or Password.')
        else:
            messages.error(request, 'Form validation failed.')
    else:
        form = LoginForm(request=request)

    return render(request, 'main/login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect('login')


# --------------------- Booking Appointment ---------------------

@login_required
def book_appointment(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    time_slots = generate_time_slots(doctor.available_from, doctor.available_to)

    if request.method == 'POST':
        date_str = request.POST.get('date')
        time_str = request.POST.get('time')

        if not date_str or not time_str:
            messages.error(request, "Please select both a date and time.")
            return redirect('book_appointment', doctor_id=doctor.id)

        appointment_date = parse_date(date_str)
        appointment_time = parse_time(time_str)

        if not appointment_date or not appointment_time:
            messages.error(request, "Invalid date or time format.")
            return redirect('book_appointment', doctor_id=doctor.id)

        naive_datetime = datetime.combine(appointment_date, appointment_time)
        appointment_datetime = timezone.make_aware(naive_datetime, timezone.get_current_timezone())

        current_datetime = timezone.localtime()
        today = current_datetime.date()
        current_time = current_datetime.time()

        if appointment_date < today:
            messages.error(request, "You cannot book appointments for past dates.")
            return redirect('book_appointment', doctor_id=doctor.id)

        if appointment_date == today and appointment_time <= current_time:
            messages.error(request, "This time slot has already passed for today.")
            return redirect('book_appointment', doctor_id=doctor.id)

        if Appointment.objects.filter(doctor=doctor, date=appointment_date, time=appointment_time).exists():
            messages.warning(request, f"The time slot {time_str} on {date_str} is already booked.")
            return redirect('book_appointment', doctor_id=doctor.id)

        Appointment.objects.create(
            user=request.user,
            doctor=doctor,
            date=appointment_date,
            time=appointment_time
        )
        messages.success(request, "Appointment booked successfully!")
        return redirect('success')

    return render(request, 'main/book_appointment.html', {
        'doctor': doctor,
        'time_slots': time_slots
    })


# --------------------- Doctor Dashboard ---------------------

# views.py

from django.shortcuts import render, get_object_or_404
from .models import Appointment, Doctor
from datetime import date

def doctor_dashboard(request):
    doctor = get_object_or_404(Doctor,user=request.user)

    today = date.today()

    appointments = Appointment.objects.filter(doctor=doctor)
    today_appointments = appointments.filter(date=today)
    upcoming_appointments = appointments.filter(date__gt=today)
    past_appointments = appointments.filter(date__lt=today)

    context = {
        'doctor': doctor,
        'appointments': appointments,
        'today_appointments': today_appointments,
        'upcoming_appointments': upcoming_appointments,
        'past_appointments': past_appointments,
    }

    return render(request, 'main/doctor_dashboard.html', context)

from django.http import HttpResponseForbidden


# def cancel_appointment(request, appointment_id):
#     # Get the appointment by its ID
#     appointment = get_object_or_404(Appointment, id=appointment_id)

#     # Ensure the logged-in doctor is the one associated with the appointment
#     if request.user != appointment.doctor :
#         return HttpResponseForbidden("You are not authorized to cancel this appointment.")

#     # Update the appointment's status to 'Cancelled'
#     appointment.status = 'Cancelled'
#     appointment.save()

#     # Add a success message
#     messages.success(request, f'Appointment with {appointment.user.username} has been cancelled.')

#     # Redirect back to the doctor dashboard
#     return redirect('doctor_dashboard')  # Change this to the actual URL name for the dashboard



from django.shortcuts import render, redirect
from .forms import DoctorForm
from django.contrib import messages

from django.shortcuts import render, redirect
from main.forms import DoctorForm
from django.contrib import messages

def add_doctor(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            doctor = form.save(commit=False)
            doctor.user = request.user  # Ensure the logged-in user is assigned to the doctor
            doctor.save()
            messages.success(request, "Doctor added successfully!")
            return redirect('doctor_dashboard')  # Redirect to the doctor's dashboard or the appropriate page
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = DoctorForm()

    return render(request, 'main/add_doctor.html', {'form': form})


