from django import forms
from .models import Tweet, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class TweetForm(forms.ModelForm):
    text = forms.CharField(required=True, widget=forms.Textarea(attrs={'placeholder': "What's going on?", 'class': "form-control"}),
    label="")

    class Meta:
        model=Tweet
        exclude = ['user','likes']

class SignUpForm(UserCreationForm):
    email = forms.EmailField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}))
    first_name = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))


    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'})
        self.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})

class ProfileImageForm(forms.ModelForm):
    profile_image = forms.ImageField(required=False, label="Profile Image")
    bio= forms.CharField(required=False, label="Bio", widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Bio'}))

    class Meta:
        model = Profile
        fields = ['profile_image', 'bio']