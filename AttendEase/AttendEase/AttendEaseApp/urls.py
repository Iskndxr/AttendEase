from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('studentMain/', views.studentMain, name='studentMain'),
    path('staffMain/', views.staffMain, name='staffMain'),
    path('updateProfile/', views.updateProfile, name='updateProfile'),
    path('', views.logout, name='logout'),
]
