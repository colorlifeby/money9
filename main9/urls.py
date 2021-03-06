"""main9 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.views.generic import TemplateView
from main9 import views

urlpatterns = [
    url(r'^template/', TemplateView.as_view(template_name="main_page.html")),
    url(r'^$', views.main_page, name='main_page'),
    url(r'^register/$', views.register_view, name='register_view'),
    url(r'^logout/$', views.logout_view, name='logout_view'),
    url(r'^login/$', views.login_view, name='login_view'),
    url(r'^userprofile/$', views.user_profile, name='user_profile'),
    url(r'^resetpassword/$', views.reset_password, name='reset_password'),
    url(r'^resetsuccess/$', views.reset_success, name='reset_success'),
]


