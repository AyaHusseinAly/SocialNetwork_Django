from django.db import models
from django.contrib.auth.models import User

class Friend(models.Model):
    users = models.ManyToManyField(User)



# Create your models here.
