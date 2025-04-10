from django import forms
from main.models import *
from django.contrib import messages
import re


def add_message(request, message_type, message_text):
    if message_type == 'success':
        messages.success(request, message_text) 
    elif message_type == 'info':
        messages.info(request, message_text)
    elif message_type == 'warning':
        messages.warning(request, message_text)
    else:
        messages.error(request, message_text)
        
class UserRegistrationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  
        super().__init__(*args, **kwargs)

    class Meta:
        model = UserRegistration
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        
        ]
        

    def clean(self):
        cleaned_data = super().clean()
        try:
            if not all(cleaned_data.values()):
                add_message(self.request, 'warning', "All fields are required.")
        except Exception as e:
            return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
                add_message(self.request, 'warning', "Invalid email format.")


            if UserRegistration.objects.filter(email=email).exists():
                add_message(self.request, 'warning', "This email address is already registered.")
                

        except Exception as e:
                add_message(self.request, 'warning', "Error")
        return email

    def clean_contact(self):
        contact = self.cleaned_data.get("contact")
        try:
            if not re.match(r"^[6-9]\d{9}$", contact):
                add_message(self.request, 'warning', "Invalid number format.")
               

        except Exception as e:
           
            raise forms.ValidationError("An error occurred during validation. Please try again.")
        return contact

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            if UserRegistration.objects.filter(username=username).exists():
                add_message(self.request, 'warning', f"Username '{username}' already exists.")
        except Exception as e:
            raise forms.ValidationError("An error occurred during validation. Please try again.")
        return username

    def clean_password(self):   
        password = self.cleaned_data.get("password")
        try:
            if not re.match(r"""^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$""", password):
                add_message(self.request, 'warning', "Invalid password format.")
                raise forms.ValidationError("Invalid password format.")
        except Exception as e:
            raise forms.ValidationError("An error occurred during validation. Please try again.")
        return password
    
    
    
    
class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        try:
            if username:
                user = UserRegistration.objects.filter(username=username).first()
                if not user:
                    add_message(self.request, 'warning', "This username does not exist.") 
                    raise forms.ValidationError("This username does not exist.")

                if not password:
                    add_message(self.request, 'warning', "A valid password is required.")
                    raise forms.ValidationError("A valid password is required.")

        except Exception as e:
            raise forms.ValidationError("An error occurred during validation. Please try again.")

        return cleaned_data