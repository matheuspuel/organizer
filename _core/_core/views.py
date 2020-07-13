from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse


@login_required(login_url='/login/')
def index(request):
    context = {}
    return render(request, 'index.html', context)


def login_view(request):

    context = {
        'next': request.GET.get('next')
    }
    return render(request, 'login.html', context)


def login_submit(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
    next_path = reverse('index')
    if request.GET:
        next_path = request.GET.get('next')
    return redirect(next_path)


def logout_submit(request):
    logout(request)
    return redirect(reverse('login'))
