from django import forms
from django.contrib.auth.forms import UserCreationForm

from photos.models import CustomUser


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=128)
    last_name = forms.CharField(max_length=128)
    email = forms.EmailField(max_length=254, help_text='Inform a valid email address.')

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)
