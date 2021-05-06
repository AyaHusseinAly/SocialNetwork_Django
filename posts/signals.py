from django.db.models.signals import post_save, pre_save, post_delete, pre_delete
from django.dispatch import receiver
from msgnotifications.models import Notification
from friend.models import FriendRequest


from .models import Comment, Like
from groups.models import GroupInvite, GroupRequestJoin


@receiver(post_save, sender=Comment)
def after_comment_creation(sender, instance, created, *args, **kwargs):
    if created:
        text = str(instance.owner.username +
                   " commented on your post: "+instance.content[0:30])
        if instance.post.owner != instance.owner:
            notify_instance = Notification.objects.create(
                sender=instance.owner, reciever=instance.post.owner, text=text, notifyType="postView_comment", instance_id=instance.post.id)
            notify_instance.save()
    else:
        print("Updating..")


@receiver(post_save, sender=GroupInvite)
def after_group_invitation(sender, instance, created, *args, **kwargs):
    if created:
        text = str(instance.inviteFrom)+" invited you to join " + \
            str(instance.group.name+" group")
        notify_instance = Notification.objects.create(
            sender=instance.inviteFrom, reciever=instance.inviteTo, text=text, notifyType="groupView", instance_id=instance.group.id)
        notify_instance.save()
    else:
        print("Updating..")


@receiver(post_save, sender=GroupRequestJoin)
def after_group_Request(sender, instance, created, *args, **kwargs):
    if created:
        text = str(instance.requestFrom)+" sent request to join " + \
            str(instance.group.name+" group")
        notify_instance = Notification.objects.create(
            sender=instance.requestFrom, reciever=instance.requestTo, text=text, notifyType="groupRequest", instance_id=instance.group.id)
        notify_instance.save()
    else:
        print("Updating..")


@receiver(post_save, sender=FriendRequest)
def after_friend_request(sender, instance, created, *args, **kwargs):
    if created:
        text = str(instance.sender.username + " sent you a friend request ")
        notify_instance = Notification.objects.create(
            sender=instance.sender, reciever=instance.receiver, text=text, notifyType="profileView", instance_id=instance.sender.id)
        notify_instance.save()
    else:
        print("Updating..")


@receiver(post_save, sender=Like)
def after_like_creation(sender, instance, created, *args, **kwargs):
    if created:
        text = str(instance.user.username+" liked your post: " +
                   instance.post.content[0:30])
        if instance.post.owner != instance.user:
            notify_instance = Notification.objects.create(
                sender=instance.user, reciever=instance.post.owner, text=text, notifyType="postView_like", instance_id=instance.post.id)
            notify_instance.save()
    else:
        print("Updating..")
