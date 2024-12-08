from django.contrib import admin
from .models import Todo, AuditLog

admin.site.register(Todo)
admin.site.register(AuditLog)

# Register your models here.
