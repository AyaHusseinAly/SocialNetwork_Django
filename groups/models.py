from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Group(models.Model):
    name=models.CharField(max_length=100)
    #name = models.CharField(max_length=255)
    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name="group")

    def __str__(self):
        return self.name