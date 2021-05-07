from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from groups.models import Group

# Create your models here.


class UserProfile(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name=models.CharField(max_length=50,null=False,blank=False)
    last_name=models.CharField(max_length=50,null=False,blank=False)
    email = models.EmailField(max_length=255, default=None,unique=True)
    country = models.CharField(max_length=30, null=True, blank=True)
    avatar = models.ImageField(null=True, blank=True)
    birthdate = models.DateField(
        auto_now=False, auto_now_add=False, null=False, blank=False)
    about = models.TextField(max_length=500, null=True, blank=True)
    groups = models.ManyToManyField(Group, blank=True, null=True)

    

    def __str__(self):
        return self.user.username
