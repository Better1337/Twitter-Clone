from django import forms
from .models import Tweet

class TweetForm(forms.ModelForm):
    text = forms.CharField(required=True, widget=forms.Textarea(attrs={'placeholder': "What's going on?", 'class': "form-control"}),
    label="")

    class Meta:
        model=Tweet
        exclude = ['user']