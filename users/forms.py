from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.shortcuts import render
from django.views import View

from users.models import User


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class UserProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'avatar', 'phone', 'country')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()

class UserPassportResetForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email',)