# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100,
                               required=False, 
                               label='Имя пользователя')
    email = forms.EmailField(required=False,
                             label='E-mail')
    password = forms.CharField(widget=forms.PasswordInput, 
                               required=False,
                               label='Пароль')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise forms.ValidationError('Не задано имя пользователя')
        try:
            User.objects.get(username=username)
            raise forms.ValidationError('Такой пользователь уже существует')
        except User.DoesNotExist:
            pass
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError('Не указан адрес электронной почты')
        try:
            User.objects.get(email=email)
            raise forms.ValidationError('Email уже используется')
        except User.DoesNotExist:
            pass
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            raise forms.ValidationError('Не указан пароль')
        self.raw_password = password
        return make_password(password)

    def save(self):
        user = User(**self.cleaned_data)
        user.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField( max_length=100, 
	                            required=False,
								label='Имя пользователя')
    password = forms.CharField(widget=forms.PasswordInput, 
	                           required=False,
							   label='Пароль')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise forms.ValidationError('Не задано имя пользователя')
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            raise forms.ValidationError('Не указан пароль')
        return password

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError('Неверное имя пользователя или пароль1')
        if not user.check_password(password):
            raise forms.ValidationError('Неверное имя пользователя или пароль2')
			