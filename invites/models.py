from django.db import models

class InviteEmails(models.Model):
    emailaddress = models.EmailField()