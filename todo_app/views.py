from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from .forms import CustomUserCreationForm
from .models import Todo
from .utils import log_user_action
import json
import logging

logger = logging.getLogger('todo_app')

@login_required
def index(request):
    todos = Todo.objects.filter(user=request.user)
    # Decrypt tasks before sending to template
    todos_data = [{
        'id': todo.id,
        'task': todo.decrypted_task,
        'completed': todo.completed
    } for todo in todos]
    return render(request, 'todo_app/index.html', {'todos': todos_data})

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)

            if user is not None:
                login(request, user)
                log_user_action(request, 'login_success', f'User logged in: {email}')
                return redirect('index')

            log_user_action(request, 'failed_login', f'Failed login attempt for email: {email}')
            return render(request, 'todo_app/login.html', {'error': 'Invalid credentials'})

        except User.DoesNotExist:
            log_user_action(request, 'failed_login', f'Login attempt with non-existent email: {email}')
            return render(request, 'todo_app/login.html', {'error': 'Invalid credentials'})
        except Exception as e:
            logger.error(f'Login error: {str(e)}')
            return render(request, 'todo_app/login.html', {'error': 'An error occurred'})

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
            'task': todo.decrypted_task,
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
        todo = get_object_or_404(Todo, id=todo_id)

        # Check if the user owns the todo
        if todo.user != request.user:
            log_user_action(request, 'unauthorized_access', f'Attempted to delete todo {todo_id}')
            raise PermissionDenied("You don't have permission to delete this todo")

        todo.delete()
        log_user_action(request, 'delete_todo', f'Deleted todo {todo_id}')
        return JsonResponse({'status': 'success'})

    return JsonResponse({'error': 'Invalid request'}, status=400)