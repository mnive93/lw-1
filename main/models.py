from django.db import models
from django.contrib.auth.models import User

class SignupHandler(models.Model):
    emailaddress = models.EmailField()
    identifiernum = models.IntegerField()
    
class Posts(models.Model):
    user = models.ForeignKey(User)
    text = models.CharField(max_length=250)
    time = models.DateTimeField(auto_now_add = True)
    popularity = models.IntegerField(default = 1)