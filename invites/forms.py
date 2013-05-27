from django import forms
from django.core.exceptions import ObjectDoesNotExist
from invites.models import InviteEmails

class InviteForm(forms.Form):
    emailaddress = forms.EmailField(label='')
    
    # Redundancy checker runs through the existing list of email addresses and checks for repeated email signups, if any and throws a validation error. In addition,
    # we can have a validation in the views.py file also.
    
    def RedundancyChecker(self):
        email = self.cleaned_data['emailaddress']
        
        try:
            InviteEmails.objects.get(emailaddress = email)
        except ObjectDoesNotExist:
            return email
        raise forms.ValidationError('Email already exists in the database.')