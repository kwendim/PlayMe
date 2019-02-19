from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Game
import backend.tokens as tokens

class SignUpForm(UserCreationForm):
    """
    The Sign-up form.
    
    Contains fields as per the User built-in model and the Profile model defined in models.py.
    """
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    is_developer = forms.BooleanField(required=False,
                                        initial=False,
                                        label = "Are you a developer?")

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'is_developer', 'password1', 'password2')

    def clean_email(self):
        """Checks if the email already exists and reports back to the user."""
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registered.")
        return email


class GameUploadForm(forms.ModelForm):
    """
    The Game upload form.
    
    Contains fields as per the Game model defined in models.py"
    """
    name = forms.CharField(max_length=30, required=True)
    category = forms.ChoiceField(choices=tokens.GAME_CATEGORIES, required=True)
    description = forms.Textarea()
    link = forms.URLField(required=True)
    price = forms.IntegerField(max_value= 100, min_value= 0, required= True)
    thumbnail = forms.ImageField(required=False)
    class Meta:
        model = Game
        fields = ('name','category', 'description', 'link','price','thumbnail')
