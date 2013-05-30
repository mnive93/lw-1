from django.db import models

class InviteEmails(models.Model):
    emailaddress = models.EmailField()
    
class TwitterEmails(models.Model):
    emailadd = models.ForeignKey(InviteEmails)
    username = models.CharField(max_length=32)