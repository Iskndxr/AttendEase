from django.shortcuts import render, redirect
from .models import CustomUser,Department,Subject,Class,ClassSession,Attendance,MCsubmission,SLsubmission
from .forms import RegistrationForm, LoginForm
from django.contrib import messages
from django.db import transaction
from django.contrib.auth import login as auth_login

# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            identifier = form.cleaned_data['identifier']
            password = form.cleaned_data['password']

            with transaction.atomic():
                CustomUser.objects.create_user(identifier=identifier, password=password, is_student=True)
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login')
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            auth_login(request, user)

            if user.is_lecturer or user.is_uttk or user.is_tphea or user.is_admin:
                return redirect('staffMain')
            
            else:
                return redirect('studentMain')
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})

def updateProfile(request):
    return render(request, 'updateProfile.html')

def studentMain(request):
    user = request.user
    return render(request, 'studentMain.html', {'user': user})

def staffMain(request):
    return render(request, 'staffMain.html')

def logout(request):
    logout(request)
    return redirect('index')