from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

class SignupFormA(forms.Form):
    email = forms.EmailField()
    
    def clean_email(self):
        email = self.cleaned_data['email']
        
        try:
            User.objects.get(email = email)
        except ObjectDoesNotExist:
            return email
        raise forms.ValidationError('This email address has been linked to another account on Likewyss.')
        
class SignupFormB(forms.Form):
    fullname = forms.CharField(max_length=64)
    username = forms.CharField(max_length=32)
    password = forms.CharField(max_length = 32, widget = forms.PasswordInput())
    
    def clean_username(self):
        user = self.cleaned_data['username']
        
        try:
            u = User.objects.get(username = user)
        except ObjectDoesNotExist:
            return user
        raise forms.ValidationError('Username already taken. Please pick another one.')