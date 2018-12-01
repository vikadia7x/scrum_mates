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
from showtimefinder.forms import EmailValidationOnForgotPassword


urlpatterns = [
    path('',views.landing,name='landing'),
    path('admin/', admin.site.urls),
    path('', views.landing, name='landing'),
    path('accounts/logout/', include('django.contrib.auth.urls')),
    path('login.html', views.login_page, name='login_page'),
    path('select.html', views.select, name='select'),
    path('signup.html', views.signup, name='signup'),
    path('home.html', views.home, name='home'),
    path('displaymovies.html',views.displaymovies, name = 'displaymovies'),
    path('userprofile.html', views.userprofile, name='userprofile'),
    path('AboutUs.html', views.AboutUs, name='AboutUs'),
    path('landing.html', views.landing, name='landing'),
    path('edit_profile.html', views.edit_profile, name='edit_profile'),
    url(r'^movie_info/$', views.movieInfo, name='movieInfo'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'', include('social_django.urls', namespace='social')),
    # url(r'^logout/$', views.logoutView, name='logout'),


    path('accounts/password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('accounts/password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(form_class=EmailValidationOnForgotPassword), name='password_reset'),

    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),



]
