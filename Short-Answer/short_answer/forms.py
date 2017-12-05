from short_answer.models import UserProfile
from django.contrib.auth.models import User
from django import forms


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    isStudent = forms.BooleanField(required=False)

    class Meta:
        model = UserProfile
        fields = ('isStudent',)
