from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Userverification(models.Model):
    uname=models.TextField(max_length=50,default=None)
    location=models.TextField(max_length=70)
    genres=models.TextField(max_length=300)
    
    

    