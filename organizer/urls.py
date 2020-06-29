"""organizer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.views.generic import RedirectView
from organizer import views

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/login/submit/', views.login_submit, name='login_submit'),
    path('accounts/logout/', views.logout_submit, name='logout'),

    path('', RedirectView.as_view(url=reverse_lazy('todolist_index')), name='index'),

    path('todolist/', include('todolist.urls'), name='todolist'),
    path('notes/', include('notes.urls'), name='notes'),
]
