from django.contrib import admin
from .models import  Doctor, Appointment ,UserRegistration

admin.site.register(Doctor)
admin.site.register(Appointment)
admin.site.register(UserRegistration)
