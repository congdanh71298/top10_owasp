from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm
from .models import Todo
import json

@login_required
def index(request):
    todos = Todo.objects.filter(user=request.user)
    return render(request, 'todo_app/index.html', {'todos': todos})

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

@login_required
def add_todo(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        todo = Todo.objects.create(
            user=request.user,
            task=data['task']
        )
        return JsonResponse({
            'id': todo.id,
            'task': todo.task,
            'completed': todo.completed
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def toggle_todo(request, todo_id):
    if request.method == 'POST':
        todo = Todo.objects.get(id=todo_id, user=request.user)
        todo.completed = not todo.completed
        todo.save()
        return JsonResponse({'completed': todo.completed})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def delete_todo(request, todo_id):
    if request.method == 'DELETE':
        Todo.objects.filter(id=todo_id, user=request.user).delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'error': 'Invalid request'}, status=400)