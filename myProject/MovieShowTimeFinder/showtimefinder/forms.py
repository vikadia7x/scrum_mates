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

    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','dateofbirth','zipcode','password1', 'password2', )

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class MovieSelection(forms.Form):
    Action = forms.BooleanField(required=False)
    Adventure = forms.BooleanField(required=False)
    Animation = forms.BooleanField(required=False)
    Comedy = forms.BooleanField(required=False)
    Crime = forms.BooleanField(required=False)
    Documentary = forms.BooleanField(required=False)
    Drama = forms.BooleanField(required=False)
    Family = forms.BooleanField(required=False)
    Fantasy = forms.BooleanField(required=False)
    History = forms.BooleanField(required=False)
    Horror = forms.BooleanField(required=False)
    Music = forms.BooleanField(required=False)
    Mystery = forms.BooleanField(required=False)
    Romance = forms.BooleanField(required=False)
    Science = forms.BooleanField(required=False)
    TV = forms.BooleanField(required=False)
    Thriller = forms.BooleanField(required=False)
    War = forms.BooleanField(required=False)
    Western = forms.BooleanField(required=False)
