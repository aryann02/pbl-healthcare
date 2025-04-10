# models.py

from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser, Permission

from django.contrib.auth.models import AbstractUser

class UserRegistration(AbstractUser):
    birth_date = models.DateField(null=True , blank= True)
    

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    available_from = models.TimeField()
    available_to = models.TimeField()

    def __str__(self):
        return self.name


class Appointment(models.Model):
    user = models.ForeignKey(UserRegistration, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return f"Appointment with {self.doctor.name} on {self.date} at {self.time}"
    
    

