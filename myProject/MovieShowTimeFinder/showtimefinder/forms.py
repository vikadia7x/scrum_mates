from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SearchForm(forms.Form):
    post = forms.CharField()

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    dateofbirth = forms.DateField(input_formats=['%Y-%m-%d'], required=True)
    zipcode = forms.CharField()
    username1 = forms.CharField()

    class Meta:
        model = User
        fields = ('username', 'username1','first_name', 'last_name', 'email','dateofbirth','zipcode','password1', 'password2', )
