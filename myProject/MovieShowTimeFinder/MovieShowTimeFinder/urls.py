"""MovieShowTimeFinder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from showtimefinder import views
from django.contrib.auth import views as auth_views

from django.views.generic.base import TemplateView
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup.html', views.signup, name='signup'),
    path('home.html', views.home, name='home'),
    # path('',views.landing, name = 'landing'),
    path('userprofile.html', views.userprofile, name='userprofile'),
    path('AboutUs.html', views.AboutUs, name='AboutUs'),
    # path('home/', TemplateView.as_view(template_name='home.html'), name='home'),
    path('landing.html', views.landing, name='landing'),
    
    # path('accounts/', auth_views.login, name='login'),

    # path(r'^accounts/', auth_views.password_reset, name='password_reset_form'),
    # url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    # url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.password_reset_confirm, name='password_reset_confirm'),
    # url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
]
