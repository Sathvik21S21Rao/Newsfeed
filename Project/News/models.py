from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Userverification(models.Model):
    def unicode( self ) :
        return self.user.username
    
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    username=models.TextField(max_length=30)
    location=models.TextField(max_length=70)
    genres=models.TextField(max_length=300)


    