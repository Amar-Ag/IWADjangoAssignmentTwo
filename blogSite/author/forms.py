from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms

from .models import Author


class CreateUserForm(UserCreationForm):
    first_name = forms.CharField(label="First Name")
    last_name = forms.CharField(label="Last Name")

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']
        required = ['first_name', 'last_name']


class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = '__all__'
        exclude = ['user']
