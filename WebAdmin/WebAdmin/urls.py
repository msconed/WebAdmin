"""
Definition of urls for WebAdmin.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('details/<str:uid>/', views.details, name='details'),
    # ----------- Steam ----------- #
    path('login/', views.login, name='login'),
    path('callback/', views.login_callback, name='callback'),
    path('logout/', views.logout, name='logout'),
    # ----------- Steam ----------- # 
    path('update_items/', views.update_items, name='update_items'),
    
]
