from django.db import models

class SignupHandler(models.Model):
    emailaddress = models.EmailField()
    identifiernum = models.IntegerField()