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
    username = forms.CharField(required=False)  # Make username optional as we'll set it automatically

    class Meta:
        model = User
        fields = ("first_name", "email", "password1", "password2")

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        if email:
            # Create a valid username from email
            base_username = email.split('@')[0]
            # Remove invalid characters and ensure it's unique
            username = re.sub(r'[^\w.]', '', base_username)
            # Ensure username is unique
            counter = 1
            temp_username = username
            while User.objects.filter(username=temp_username).exists():
                temp_username = f"{username}{counter}"
                counter += 1
            cleaned_data['username'] = temp_username
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.username = self.cleaned_data["username"]
        user.first_name = self.cleaned_data["first_name"]
        if commit:
            user.save()
        return user

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email
