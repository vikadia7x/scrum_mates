from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from showtimefinder.models import UserProfile
from django.forms import ModelForm
from betterforms.multiform import MultiModelForm

class SearchForm(forms.Form):
    post = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Enter zipcode','style':'height:50px', 'size':'80'}))

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    dateofbirth = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    zipcode = forms.CharField()

    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','dateofbirth','zipcode','password1', 'password2', )

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class MovieSelection(forms.Form):
    Action = forms.BooleanField(label_suffix='',required=False, widget=forms.CheckboxInput(attrs={'class':"checkbox style-2 pull-left",'style':"margin: 5px 10px 0px 3px;"}))
    Adventure = forms.BooleanField(label_suffix='',required=False, widget=forms.CheckboxInput(attrs={'class':"checkbox style-2 pull-left",'style':"margin: 5px 10px 0px 3px;"}))
    Animation = forms.BooleanField(label_suffix='',required=False, widget=forms.CheckboxInput(attrs={'class':"checkbox style-2 pull-left",'style':"margin: 5px 10px 0px 3px;"}))
    Comedy = forms.BooleanField(label_suffix='',required=False,widget=forms.CheckboxInput(attrs={'class':"checkbox style-2 pull-left",'style':"margin: 5px 10px 0px 3px;"}))
    Crime = forms.BooleanField(label_suffix='',required=False,widget=forms.CheckboxInput(attrs={'class':"checkbox style-2 pull-left",'style':"margin: 5px 10px 0px 3px;"}))
    Documentary = forms.BooleanField(label_suffix='',required=False,widget=forms.CheckboxInput(attrs={'class':"checkbox style-2 pull-left",'style':"margin: 5px 10px 0px 3px;"}))
    Drama = forms.BooleanField(label_suffix='',required=False, widget=forms.CheckboxInput(attrs={'class':"checkbox style-2 pull-left",'style':"margin: 5px 10px 0px 3px;"}))
    Family = forms.BooleanField(label_suffix='',required=False, widget=forms.CheckboxInput(attrs={'class':"checkbox style-2 pull-left",'style':"margin: 5px 10px 0px 3px;"}))
    Fantasy = forms.BooleanField(label_suffix='',required=False, widget=forms.CheckboxInput(attrs={'class':"checkbox style-2 pull-left",'style':"margin: 5px 10px 0px 3px;"}))
    Horror = forms.BooleanField(label_suffix='',required=False, widget=forms.CheckboxInput(attrs={'class':"checkbox style-2 pull-left",'style':"margin: 5px 10px 0px 3px;"}))
    Music = forms.BooleanField(label_suffix='',required=False, widget=forms.CheckboxInput(attrs={'class':"checkbox style-2 pull-left",'style':"margin: 5px 10px 0px 3px;"}))
    Mystery = forms.BooleanField(label_suffix='',required=False, widget=forms.CheckboxInput(attrs={'class':"checkbox style-2 pull-left",'style':"margin: 5px 10px 0px 3px;"}))
    Romance = forms.BooleanField(label_suffix='',required=False, widget=forms.CheckboxInput(attrs={'class':"checkbox style-2 pull-left",'style':"margin: 5px 10px 0px 3px;"}))
    Science = forms.BooleanField(label_suffix='',required=False, widget=forms.CheckboxInput(attrs={'class':"checkbox style-2 pull-left",'style':"margin: 5px 10px 0px 3px;"}))
    TV = forms.BooleanField(label_suffix='',required=False, widget=forms.CheckboxInput(attrs={'class':"checkbox style-2 pull-left",'style':"margin: 5px 10px 0px 3px;"}))
    Thriller = forms.BooleanField(label_suffix='',required=False, widget=forms.CheckboxInput(attrs={'class':"checkbox style-2 pull-left",'style':"margin: 5px 10px 0px 3px;"}))
    War = forms.BooleanField(label_suffix='',required=False, widget=forms.CheckboxInput(attrs={'class':"checkbox style-2 pull-left",'style':"margin: 5px 10px 0px 3px;"}))
    Western = forms.BooleanField(label_suffix='',required=False, widget=forms.CheckboxInput(attrs={'class':"checkbox style-2 pull-left",'style':"margin: 5px 10px 0px 3px;"}))

class EditProfileForm(ModelForm):

    class Meta:
        model = User
        exclude = ['password']
        fields = (
            'email',
            'first_name',
            'last_name',
)

class EditUserProfileForm(ModelForm):

    class Meta:
        model = UserProfile
        fields = (
            'dateofbirth',
            'zipcode',
        )

# class UserEditMultiForm(MultiModelForm):
#     form_classes = {
#         'user': EditProfileForm,
#         'profile': EditUserProfileForm,
#     }