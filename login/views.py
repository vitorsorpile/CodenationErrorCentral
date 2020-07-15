from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from login.forms import RegistrationForm, UserAuthenticationForm

def login_view(request):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect('index')

    if request.POST:
        form = UserAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']

            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect('index')
    else:
        form = UserAuthenticationForm()

    context['login_form'] = form
    return render(request, 'login.html', context)

def register_view(request):
    user = request.user
    if user.is_authenticated:
        return redirect('index')
    
    context = {}

    if request.POST:
        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            return redirect('index')

        else: 
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form

    return render(request, 'register.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')


