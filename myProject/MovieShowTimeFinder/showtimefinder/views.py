from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from showtimefinder.forms import SignUpForm
from showtimefinder.models import User

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        obj = User()
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            user.save()
            obj.first_name = form.cleaned_data['first_name']
            obj.last_name = form.cleaned_data['last_name']
            obj.email = form.cleaned_data['email']
            obj.dateofbirth = form.cleaned_data['dateofbirth']
            obj.save()
            #login(request, user)
            return redirect('home.html')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def landing(request):
    return render(request,'landing.html')

def home(request):
    return render(request,'home.html')
