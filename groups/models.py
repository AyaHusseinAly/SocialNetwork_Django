from django.db import models
from django.contrib.auth.models import User
import datetime


# Create your models here.


class Group(models.Model):
    CHOICES = (
        ('pub', 'public'),
        ('fr', 'friends'),
    )
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="group")
    privacy = models.CharField(max_length=300, choices=CHOICES)
    description = models.CharField(max_length=1000)
    cover = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name


class GroupInvite(models.Model):
    created_at = datetime.datetime.now()
    inviteFrom = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="groupinvitefrom")
    inviteTo = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="groupinviteto")
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name="groupinvitegroup")

    def __str__(self):
        return str(self.inviteFrom) + " invited " + str(self.inviteTo) + " to join " + str(self.group.name)


class GroupRequestJoin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    requestFrom = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="grouprequestjoinfrom")
    requestTo = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="grouprequestjointo")
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name="grouprequestjoingroup")

    def __str__(self):
        return str(self.requestFrom) + " requested to join " + str(self.group.name)
