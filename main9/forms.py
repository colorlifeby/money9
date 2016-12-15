# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=30,
                               required=True, 
                               label='Имя пользователя')
    email = forms.EmailField(required=True,
                             label='E-mail')
    password = forms.CharField(widget=forms.PasswordInput, 
                               required=True,
                               label='Пароль')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            User.objects.get(username=username)
            raise forms.ValidationError('Такой пользователь уже существует')
        except User.DoesNotExist:
            pass
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            User.objects.get(email=email)
            raise forms.ValidationError('Email уже используется')
        except User.DoesNotExist:
            pass
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        self.raw_password = password
        return make_password(password)

    def save(self):
        user = User(**self.cleaned_data)
        user.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField( max_length=30, 
                                required=True,
                                label='Имя пользователя')
    password = forms.CharField(widget=forms.PasswordInput, 
                               required=True,
                               label='Пароль')

    def clean_username(self):
        username = self.cleaned_data.get('username')
#        if not username:
#            raise forms.ValidationError('Не задано имя пользователя')
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        return password

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError('Неверное имя пользователя или пароль')
        if not user.check_password(password):
            raise forms.ValidationError('Неверное имя пользователя или пароль')

            
class UserProfileForm(forms.Form):
    
    emailnew = forms.EmailField(required=False,
                                 label='Новый E-mail')
    passwordnew = forms.CharField(widget=forms.PasswordInput, 
                                  required=False,
                                  label='Новый пароль')
    password = forms.CharField(widget=forms.PasswordInput, 
                               required=True,
                               label='Текущий пароль')       
    
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(UserProfileForm, self).__init__(*args, **kwargs)

    def clean_emailnew(self):
        email = self.cleaned_data.get('emailnew')
#        if not emailnew:
#            raise forms.ValidationError('Не указан адрес электронной почты')
        try:
            User.objects.get(email=email)
            raise forms.ValidationError('Email уже используется')
        except User.DoesNotExist:
            pass
        return email            
        
    def clean_passwordnew(self):
        password = self.cleaned_data.get('passwordnew')
        return password
        
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not self.user.check_password(password):
            raise forms.ValidationError('Неверное имя пользователя или пароль')
        return password
		
    def clean(self):
        emailnew = self.cleaned_data.get('emailnew')
        passwordnew = self.cleaned_data.get('passwordnew')
        password = self.cleaned_data.get('password')
        if not emailnew and not passwordnew:
            raise forms.ValidationError('Новые поля пустые!')        

            
class ResetPasswordForm(forms.Form):
    username = forms.CharField( max_length=30, 
                                required=True,
                                label='Имя пользователя')
    email = forms.EmailField(required=True,
                             label='E-mail')
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        return username
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        return email     

    def clean(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError('Такой пользователь в системе не зарегистрирован')
        if user.email != email:
            raise forms.ValidationError('Пользователь с таким E-mail отсутствует')


	
            