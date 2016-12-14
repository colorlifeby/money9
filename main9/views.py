from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
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
        print(form)
    return render(request, 'register.html', {'form': form,
                                             'user': request.user,
                                             'session': request.session, }) 

def login_view(request):
    if request.method == "POST":
        form = forms9.LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            # print(username, password)
            user = authenticate(username=username, password=password)
            # print(type(user))
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
        form = forms9.UserProfileForm(request.POST)
#        print request.user
        if form.is_valid():
            emailnew = form.cleaned_data["emailnew"]
            passwordnew = form.cleaned_data["passwordnew"]		
            u = request.user
            u.email=emailnew
            u.save()
            return HttpResponseRedirect('/')
    else:
        form = forms9.UserProfileForm()
    return render(request, 'profile.html', {'form': form,
                                            'user': request.user,
                                            'session': request.session, })
											
											
											
											
											
											