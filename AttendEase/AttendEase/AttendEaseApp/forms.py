import re
from django import forms
from django.core.exceptions import ValidationError
from .models import CustomUser
from django.contrib.auth import authenticate, login

class RegistrationForm(forms.Form):
    identifier = forms.CharField(
        label='Matric ID', 
        max_length=11, 
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'e.g., XXX0000-000'})
    )
    password = forms.CharField(
        help_text='Your password must contain at least 8 characters including an uppercase letter, a lowercase letter, and a number.',
        label='Password', 
        widget=forms.PasswordInput
    )
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    def clean_identifier(self):
        identifier = self.cleaned_data['identifier']
        if not re.match(r'^[A-Z]{3}\d{4}-\d{3}$', identifier):
            raise ValidationError('Invalid Matric ID format. Expected format: XXX0000-000')

        if CustomUser.objects.filter(identifier=identifier).exists():
            raise ValidationError('User already exists')

        return identifier

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 8:
            raise ValidationError('Password must be at least 8 characters long.')
        if not re.search(r'[A-Z]', password):
            raise ValidationError('Password must contain at least one uppercase letter.')
        if not re.search(r'[a-z]', password):
            raise ValidationError('Password must contain at least one lowercase letter.')
        if not re.search(r'\d', password):
            raise ValidationError('Password must contain at least one number.')
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise ValidationError('Passwords do not match')

        return cleaned_data

class LoginForm(forms.Form):
    identifier = forms.CharField(
        label='Username', 
        max_length=11, 
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Matric ID / Staff ID'})
    )
    password = forms.CharField(
        label='Password', 
        widget=forms.PasswordInput
    )

    def clean(self):
        cleaned_data = super().clean()
        identifier = cleaned_data.get('identifier')
        password = cleaned_data.get('password')

        user = authenticate(username=identifier, password=password)
        if not user:
            raise forms.ValidationError('Invalid username or password')

        cleaned_data['user'] = user
        return cleaned_data