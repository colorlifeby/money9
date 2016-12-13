from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth import authenticate, login, logout
from main9 import forms as forms9


# Create your views here.

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
