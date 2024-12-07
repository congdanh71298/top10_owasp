from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm

@login_required
def index(request):
    return render(request, 'todo_app/index.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # Use filter instead of get to handle multiple users
            users = User.objects.filter(email=email)
            if not users.exists():
                return render(request, 'todo_app/login.html', {'error': 'User does not exist'})

            # Try to authenticate with each user's username
            for user in users:
                user = authenticate(request, username=user.username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('index')

            return render(request, 'todo_app/login.html', {'error': 'Invalid credentials'})

        except Exception as e:
            return render(request, 'todo_app/login.html', {'error': 'An error occurred during login'})

    return render(request, 'todo_app/login.html')

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'todo_app/register.html', {'error': form.errors})
    return render(request, 'todo_app/register.html')