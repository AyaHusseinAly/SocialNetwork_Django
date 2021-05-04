from django.db.models.signals import post_save, pre_save, post_delete, pre_delete
from django.dispatch import receiver
from msgnotifications.models import Notification

from .models import Comment
from groups.models import GroupInvite

@receiver(post_save, sender=Comment)
def after_comment_creation(sender,instance,created,*args,**kwargs):
    if created:
        text=str("comment from " + instance.owner.username+": "+instance.content[0:30])
        if instance.post.owner != instance.owner:
            notify_instance = Notification.objects.create(sender=instance.owner, reciever=instance.post.owner,text=text, notifyType="postView_comment",instance_id=instance.post.id)
            notify_instance.save()
    else:
        print("Updating..")




@receiver(post_save, sender=GroupInvite)
def after_comment_creation(sender,instance,created,*args,**kwargs):
    if created:
        text=str(instance.inviteFrom)+" invited you to join " + str(instance.group.name+" group")
        notify_instance = Notification.objects.create(sender=instance.inviteFrom, reciever=instance.inviteTo,text=text, notifyType="groupView",instance_id=instance.group.id)
        notify_instance.save()
    else:
        print("Updating..")

#model GroupInvite >>    inviteFrom  -  inviteTo  -  group