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
        self.request = kwargs.pop('request', None)  # Pass request as argument
        super().__init__(*args, **kwargs)

    class Meta:
        model = UserRegistration
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
            "birth_date",
            'role',
            'gender',
            'contact'
        ]

    def clean(self):
        cleaned_data = super().clean()

        # Ensure all fields have data
        if not all(cleaned_data.values()):
            add_message(self.request, messages.WARNING, "All fields are required.")
            raise forms.ValidationError("Please fill out all fields.")  # Add a general error for unfilled fields

        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email:
            # Validate email format
            if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
                add_message(self.request, "warning", "Invalid email format.")
                raise forms.ValidationError("Invalid email format.")
            # Check if email already exists in the database
            if UserRegistration.objects.filter(email=email).exists():
                add_message(self.request, "warning", "This email is already registered.")
                raise forms.ValidationError("This email is already registered.")
        return email

    def clean_contact(self):
        contact = self.cleaned_data.get("contact")
        if contact:
            # Validate mobile number format
            if not re.match(r"^[6-9]\d{9}$", contact):
                add_message(self.request, "warning", "Invalid mobile number format.")
                raise forms.ValidationError("Invalid mobile number format.")
            # Check if contact already exists in the database
            if UserRegistration.objects.filter(contact=contact).exists():
                add_message(self.request, "warning", "This contact number is already registered.")
                raise forms.ValidationError("This contact number is already registered.")
        return contact

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            # Check if username already exists in the database
            if UserRegistration.objects.filter(username=username).exists():
                add_message(self.request, "warning", f"Username '{username}' is already taken.")
                raise forms.ValidationError(f"Username '{username}' is already taken.")
        return username

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if password:
            # Validate password format: at least one lowercase, one uppercase, one number, and one special character
            if not re.match(r"""^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$""", password):
                add_message(self.request, "warning", "Invalid password format.")
                raise forms.ValidationError("Password must be at least 8 characters long, contain both uppercase and lowercase letters, a number, and a special character.")
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
    
    
    
    



class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['name', 'specialization', 'location', 'available_from', 'available_to']

