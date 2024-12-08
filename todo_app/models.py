from django.db import models
from django.contrib.auth.models import User
from .crypto import encrypt_text, decrypt_text

class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.TextField()
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        # Only encrypt if it's a new todo or task has changed
        if hasattr(self, '_decrypted_task'):
            # Re-encrypt only if task was changed
            self.task = encrypt_text(self._decrypted_task)
        elif self.task and not self.id:
            # New todo being created
            self.task = encrypt_text(self.task)
        super().save(*args, **kwargs)

    @property
    def decrypted_task(self):
        if not hasattr(self, '_decrypted_task'):
            self._decrypted_task = decrypt_text(self.task) if self.task else None
        return self._decrypted_task

    @decrypted_task.setter
    def decrypted_task(self, value):
        self._decrypted_task = value
        self.task = encrypt_text(value) if value else None

class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=50)  # e.g. 'login', 'create_todo', 'delete_todo'
    detail = models.TextField()
    ip_address = models.GenericIPAddressField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
