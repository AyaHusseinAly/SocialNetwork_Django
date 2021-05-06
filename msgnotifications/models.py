from django.db import models
from django.contrib.auth.models import User


class Notification(models.Model):
    sender=models.ForeignKey(User,on_delete=models.CASCADE,related_name="notificationSender")
    reciever=models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name="notificationReceiver")
    text=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    instance_id=models.CharField(max_length=4)
    notifyType=models.CharField(max_length=50) #group >> group Page / (comment - like -groupPost)>>post view page / friendrequest >> user profile
    read=models.BooleanField(default=False)
#### strings: postView groupView profileView
    def __str__(self):
        return str(self.sender) +" to "+ str(self.reciever)

class Message(models.Model):
    sender=models.ForeignKey(User,on_delete=models.CASCADE,related_name="messageSender")
    reciever=models.ForeignKey(User,on_delete=models.CASCADE,related_name="messageReceiver")
    text=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    read=models.BooleanField(default=False)


    def __str__(self):
        return str(self.sender)+" to "+ str(self.reciever)
