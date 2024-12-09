from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied, ValidationError
from .forms import CustomUserCreationForm, TodoForm
from .models import Todo
from .utils import log_user_action, rate_limit, validate_object_access
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

@rate_limit('login', max_requests=5, timeout=300)
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        if not email or not password:
            return render(request, 'todo_app/login.html', {'error': 'Email and password are required'})

        try:
            user = User.objects.get(email__exact=email)
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

@rate_limit('register', max_requests=3, timeout=600)
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            context = {
                'error': form.errors,
                'first_name': request.POST.get('first_name', ''),
                'email': request.POST.get('email', '')
            }
            return render(request, 'todo_app/register.html', context)
    return render(request, 'todo_app/register.html')

@login_required
def add_todo(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            form = TodoForm(data)

            if form.is_valid():
                todo = Todo.objects.create(
                    user=request.user,
                    task=form.cleaned_data['task']
                )
                return JsonResponse({
                    'id': todo.id,
                    'task': todo.decrypted_task,
                    'completed': todo.completed
                })
            return JsonResponse({'error': form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            logger.error(f'Add todo error: {str(e)}')
            return JsonResponse({'error': 'An error occurred'}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def toggle_todo(request, todo_id):
    try:
        todo = Todo.objects.get(id=todo_id)

        # Add authorization check
        if todo.user != request.user:
            return JsonResponse({'error': 'Unauthorized'}, status=403)

        todo.completed = not todo.completed
        todo.save()
        return JsonResponse({'status': 'success'})

    except Todo.DoesNotExist:
        return JsonResponse({'error': 'Todo not found'}, status=404)
    except Exception as e:
        logger.error(f"Toggle todo error: {str(e)}")
        return JsonResponse({'error': 'Server error'}, status=500)

@login_required
def delete_todo(request, todo_id):
    if request.method == 'DELETE':
        try:
            todo = get_object_or_404(Todo, id=todo_id)
            validate_object_access(todo, request.user)
            # Check if the user owns the todo
            if todo.user != request.user:
                log_user_action(request, 'unauthorized_access', f'Attempted to delete todo {todo_id}')
                raise PermissionDenied("You don't have permission to delete this todo")

            todo.delete()
            log_user_action(request, 'delete_todo', f'Deleted todo {todo_id}')
            return JsonResponse({'status': 'success'})

        except PermissionDenied as e:
            return JsonResponse({'error': str(e)}, status=403)
        except Exception as e:
            logger.error(f'Delete todo error: {str(e)}')
            return JsonResponse({'error': 'An error occurred'}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)