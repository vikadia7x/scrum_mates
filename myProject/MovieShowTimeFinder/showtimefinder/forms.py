from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User


class SearchForm(forms.Form):
    post = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Enter zipcode','size': 80}))

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    dateofbirth = forms.DateField(input_formats=['%Y-%m-%d'], required=True, help_text='Format:YYYY-MM-DD')
    zipcode = forms.CharField()

    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','dateofbirth','zipcode','password1', 'password2', )

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class MovieSelection(forms.Form):
    Action = forms.BooleanField(label_suffix='',required=False, widget=forms.CheckboxInput(attrs={'class':"checkbox style-4 pull-left"}))
    Adventure = forms.BooleanField(label_suffix='',required=False, widget=forms.CheckboxInput(attrs={'class':"checkbox style-2 pull-left"}))
    Animation = forms.BooleanField(label_suffix='',required=False, widget=forms.CheckboxInput(attrs={'class':"checkbox style-2 pull-left"}))
    Comedy = forms.BooleanField(label_suffix='',required=False,widget=forms.CheckboxInput(attrs={'class':"checkbox style-2 pull-left"}))
    Crime = forms.BooleanField(label_suffix='',required=False,widget=forms.CheckboxInput(attrs={'class':"checkbox style-2 pull-left"}))
    Documentary = forms.BooleanField(label_suffix='',required=False,widget=forms.CheckboxInput(attrs={'class':"checkbox style-2 pull-left"}))
    Drama = forms.BooleanField(label_suffix='',required=False, widget=forms.CheckboxInput(attrs={'class':"checkbox style-2 pull-left"}))
    Family = forms.BooleanField(label_suffix='',required=False, widget=forms.CheckboxInput(attrs={'class':"checkbox style-2 pull-left"}))
    Fantasy = forms.BooleanField(label_suffix='',required=False, widget=forms.CheckboxInput(attrs={'class':"checkbox style-2 pull-left"}))
    History = forms.BooleanField(label_suffix='',required=False, widget=forms.CheckboxInput(attrs={'class':"checkbox style-2 pull-left"}))
    Horror = forms.BooleanField(label_suffix='',required=False, widget=forms.CheckboxInput(attrs={'class':"checkbox style-2 pull-left"}))
    Music = forms.BooleanField(label_suffix='',required=False, widget=forms.CheckboxInput(attrs={'class':"checkbox style-2 pull-left"}))
    Mystery = forms.BooleanField(label_suffix='',required=False, widget=forms.CheckboxInput(attrs={'class':"checkbox style-2 pull-left"}))
    Romance = forms.BooleanField(label_suffix='',required=False, widget=forms.CheckboxInput(attrs={'class':"checkbox style-2 pull-left"}))
    Science = forms.BooleanField(label_suffix='',required=False, widget=forms.CheckboxInput(attrs={'class':"checkbox style-2 pull-left"}))
    TV = forms.BooleanField(label_suffix='',required=False, widget=forms.CheckboxInput(attrs={'class':"checkbox style-2 pull-left"}))
    Thriller = forms.BooleanField(label_suffix='',required=False, widget=forms.CheckboxInput(attrs={'class':"checkbox style-2 pull-left"}))
    War = forms.BooleanField(label_suffix='',required=False, widget=forms.CheckboxInput(attrs={'class':"checkbox style-2 pull-left"}))
    Western = forms.BooleanField(label_suffix='',required=False, widget=forms.CheckboxInput(attrs={'class':"checkbox style-2 pull-left"}))

class EditProfileForm(UserChangeForm):
    template_name='/something/else'

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
)
