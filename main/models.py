# models.py
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser, Permission

ROLE_CHOICES = [
    ("DOCTOR", "Doctor"),
    ("PATIENT", "Patient"),
]

GENDER_CHOICES = [
    ("MALE", "Male"),
    ("FEMALE", "Female"),
    ("OTHER", "Other"),
]

class UserRegistration(AbstractUser):
    birth_date = models.DateField(null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="PATIENT")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default="MALE")
    contact = models.CharField(max_length=15, null=True, blank=True, unique=True) 

    def __str__(self):
        return self.username

    

class Doctor(models.Model):
    user = models.OneToOneField(UserRegistration, on_delete=models.CASCADE)  # Linking Doctor to User
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    available_from = models.TimeField()
    available_to = models.TimeField()

    def __str__(self):
        return self.name


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Booked', 'Booked'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(UserRegistration, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Booked')
    notes = models.TextField(blank=True, null=True)
    is_confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Appointment with {self.doctor.name} on {self.date} at {self.time}"

    
    


