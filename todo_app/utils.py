from .models import AuditLog
from django.core.cache import cache
from functools import wraps
from django.http import HttpResponseForbidden
import time

def log_user_action(request, action, detail):
    AuditLog.objects.create(
        user=request.user if request.user.is_authenticated else None,
        action=action,
        detail=detail,
        ip_address=get_client_ip(request)
    )

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def rate_limit(key_prefix, max_requests=5, timeout=60):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped(request, *args, **kwargs):
            # Create unique key for user/IP
            key = f"{key_prefix}:{request.META.get('REMOTE_ADDR')}_{request.user.id if request.user.is_authenticated else 'anon'}"

            # Check rate limit
            requests = cache.get(key, 0)
            if requests >= max_requests:
                return HttpResponseForbidden(f"Rate limit exceeded. Please try again in {timeout} seconds.")

            # Increment requests
            cache.set(key, requests + 1, timeout)
            return view_func(request, *args, **kwargs)
        return wrapped
    return decorator

def validate_object_access(obj, user):
    """Centralized access control check"""
    if not user.is_authenticated or obj.user != user:
        raise PermissionError("Unauthorized access")
    return True