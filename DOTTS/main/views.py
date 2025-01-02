from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegistrationForm, UserLoginForm
from .models import UserProfile
from django.contrib.auth.models import User

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']

            # Check if the username already exists
            if User.objects.filter(username=username).exists():
                form.add_error('username', 'A user with this username already exists.')
                return render(request, 'main/register.html', {'form': form})

            # Check if the email already exists (optional)
            if User.objects.filter(email=email).exists():
                form.add_error('email', 'A user with this email already exists.')
                return render(request, 'main/register.html', {'form': form})

            # Save the new user first
            user = form.save(commit=False)
            user.save()  # Save the user to the database

            # Log in the user immediately after registration
            # login(request, user)  # Log in the user
            return redirect('main:home')  # Redirect to the home page after login
    else:
        form = UserRegistrationForm()
    return render(request, 'main/register.html', {'form': form})
def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('main:home')  # Redirect to a home page or dashboard after login
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = UserLoginForm()
    return render(request, 'main/login.html', {'form': form})

# def user_logout(request):
#     logout(request)
#     return redirect('main:home')

def home(request):
    return render(request, 'main/home.html')
