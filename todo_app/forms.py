from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, RegexValidator
import re

class TodoForm(forms.Form):
    task = forms.CharField(
        validators=[
            MinLengthValidator(1),
            RegexValidator(
                regex=r'^[\w\s.,!?()-]+$',
                message='Task contains invalid characters'
            )
        ],
        max_length=500
    )

    def clean_task(self):
        task = self.cleaned_data['task']
        # Additional sanitization if needed
        task = re.sub(r'[^\w\s.,!?()-]', '', task)
        return task

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"]
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        if commit:
            user.save()
        return user

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.match(r'^[\w.@+-]+$', username):
            raise forms.ValidationError("Username can only contain letters, numbers, and @/./+/-/_ characters.")
        return username