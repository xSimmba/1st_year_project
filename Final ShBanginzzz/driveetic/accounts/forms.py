
from urllib import request
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect

from accounts.views import Login

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm



class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    def init(self, args, **kwargs):
        super().init(args, **kwargs)
        self.fields['username'].widget.attrs.update({'autofocus': True})