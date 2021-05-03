from django.db import models
from django.contrib.auth.models import User


class Notification(models.Model):
    sender=models.ForeignKey(User,on_delete=models.CASCADE,related_name="notificationSender")
    reciever=models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name="notificationReceiver")
    text=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.sender) +" to "+ str(self.reciever)

class Message(models.Model):
    sender=models.ForeignKey(User,on_delete=models.CASCADE,related_name="messageSender")
    reciever=models.ForeignKey(User,on_delete=models.CASCADE,related_name="messageReceiver")
    text=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.sender)+" to "+ str(self.reciever)
