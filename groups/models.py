from django.db import models
from django.contrib.auth.models import User
from accounts.models import UserProfile

# Create your models here.


class Group(models.Model):
    CHOICES = (
        ('pub', 'public'),
        ('fr', 'friends'),
    )
    name = models.CharField(max_length=100)
    # name = models.CharField(max_length=255)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="group")
    privacy = models.CharField(max_length=300, choices=CHOICES)
    description = models.CharField(max_length=1000)
    cover = models.ImageField(null=True, blank=True)
    members = models.ManyToManyField(
        UserProfile, null=True, blank=True)

    def __str__(self):
        return self.name
