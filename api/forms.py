from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import VerifyCodeM


class SignUpForm(forms.ModelForm):
    #username = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=200)
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('username', 'email', 'password' )
class verifiedForm(forms.ModelForm):
    class Meta:
        model=VerifyCodeM
        fields=('code',)
class LoginForm(forms.ModelForm):
    email = forms.EmailField(max_length=200,initial='@gmail.com')
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model=User
        fields=('email','password')


