# -*- coding: utf-8 -*-

import random
import string
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.core.mail import send_mail
from main9 import forms as forms9


# Create your views here.
@login_required(login_url='/login/')
def main_page(request):
    return render(request, 'main_page.html', {'user': request.user,
                                              'session': request.session, })

def register_view(request):
    if request.method == "POST":
        form = forms9.RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data["username"]
            password = form.raw_password
#            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
            return HttpResponseRedirect('/')
    else:
        form = forms9.RegisterForm()
        
    return render(request, 'register.html', {'form': form,
                                             'user': request.user,
                                             'session': request.session, }) 

def login_view(request):
    if request.method == "POST":
        form = forms9.LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
            return HttpResponseRedirect('/')
    else:
        form = forms9.LoginForm()
    return render(request, 'login.html', {'form': form,
                                          'user': request.user,
                                          'session': request.session, })                                             
                                             
def logout_view(request):
            logout(request)
            return HttpResponseRedirect('/')
            

@login_required(login_url='/login/')
def user_profile(request):
    if request.method == "POST":
        form = forms9.UserProfileForm(request.user, request.POST)
        if form.is_valid():
            emailnew = form.cleaned_data["emailnew"]
            passwordnew = form.cleaned_data["passwordnew"]
            u = request.user			
            if emailnew:
                u.email=emailnew
                u.save()
            if passwordnew:
                u.set_password(passwordnew)
                u.save()				
                update_session_auth_hash(request, u)
            return HttpResponseRedirect('/')
    else:
        form = forms9.UserProfileForm(request.user)
    return render(request, 'profile.html', {'form': form,
                                            'user': request.user,
                                            'session': request.session, })
											
def reset_password(request):
    if request.method == "POST":
        form = forms9.ResetPasswordForm(request.POST)
        if form.is_valid():
            token = ''.join(random.choice(string.ascii_uppercase + 
            string.ascii_lowercase + string.digits) for x in range(5))
            
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            u = User.objects.get(username=username)
            u.set_password(token)
            u.save()            
            print 'Send email'
            print token
            send_mail('Новый пароль', token, settings.EMAIL_HOST_USER, ['aleks.by@mail.ru'])
            return HttpResponseRedirect('/resetsuccess/')
    else:
        form = forms9.ResetPasswordForm()
    return render(request, 'resetpassword.html', {'form': form,
                                                  'user': request.user,
                                                  'session': request.session, })
											
def reset_success(request):
    return render(request, 'resetsuccess.html', { 'user': request.user,
                                                  'session': request.session, })											
											
											
											