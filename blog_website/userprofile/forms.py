
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import fields
from . models import UserProfile

class SignUpForm(UserCreationForm):
  class Meta:
    model=User
    fields=('username','email','first_name','last_name')


class UserProfileForm(forms.ModelForm):
  date_of_birth=forms.DateField(widget=forms.TextInput(attrs={'type':'date'}))
  class Meta:
    model=UserProfile
    exclude=('user',)
