from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Game

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    is_developer = forms.BooleanField(required=False,
                                        initial=False,
                                        label = "Are you a developer?")

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'is_developer', 'password1', 'password2')


class GameUploadForm(forms.ModelForm):
    name = forms.CharField(max_length=30, required=True)
    category = forms.CharField(max_length=30, required=True)
    description = forms.CharField(widget=forms.Textarea, required=True)
    link = forms.URLField(required=True)
    price = forms.IntegerField(max_value= 100, min_value= 0, required= True)
    thumbnail = forms.ImageField(required=False)
    class Meta:
        model = Game
        fields = ('name','category', 'description', 'link','price','thumbnail')
