from django.contrib.auth.models import User
from django import forms
from .models import Blogger


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class BloggerProfileForm(forms.ModelForm):
    class Meta:
        model = Blogger
        fields = ['bio']