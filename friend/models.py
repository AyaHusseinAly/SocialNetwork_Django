from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from msgnotifications.models import Notification
import datetime

class FriendList(models.Model):
    # one friend list to one user 
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user" )
    friends = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='friendds' )

    def __str__(self):
        return self.user.username
    
    def add_friend(self, account):
        # Add a new friend

        if not account in self.friends.all():
            self.friends.add(account)
    
    def remove_friend(self, account):
        #Remove a friend 
         if account in self.friends.all():
            self.friends.remove(account)

    def unfriend(self, removee):
        #Initiate the action of unfriending someone.
        remover_friends_list = self #person terminating the friendship
        # Remove friend from remover friend list
        remover_friends_list.remove_friend(removee)

        # Remove friend from removee friend list
        friends_list = FriendList.objects.get(user=removee)
        friends_list.remove_friend(self.user)

    def is_mutual_friend(self, friend):
        # is this a friend?
        if friend in self.friends.all():
            return True
        return False

class FriendRequest(models.Model):
    
    # A friend request consists of two main parts:
    #    1. SENDER:
    #        - Person sending/initiating the friend request 
    #    2. RECEIVER:
    #        - Person receiving the friend request

    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="receiver")
    is_active = models.BooleanField(blank=True, null=False, default=True)
    timestamp=datetime.datetime.now()

    def __str__(self):
        return self.sender.username

    def accept(self):
        # Accept a friend request
        # update both DENDER and RECEIVER friend lists
        receiver_friend_list = FriendList.objects.get(user=self.receiver)
        if receiver_friend_list:
            receiver_friend_list.add_friend(self.sender)
            sender_friend_list = FriendList.objects.get(user=self.sender)
            if sender_friend_list:
                sender_friend_list.add_friend(self.receiver)
                self.is_active = False
                self.save()
                text=str(self.receiver.username +" accepted your friend request")
                notify_instance = Notification.objects.create(sender=self.receiver, reciever=self.sender,text=text, notifyType="profileView",instance_id=self.receiver.id)
                notify_instance.save()
    
    def decline(self):
        # Decline a friend request
        #it is declined by setting the 'is_active' field to False
        self.is_active = False
        self.save()

    def cancel(self):
        #cancel a friend request
        # it is 'cancelled' by setting the 'is_active' field to False
        # this is only different with respect "declining" through the notification that 
        # is genertated
        self.is_active = False
        self.save()