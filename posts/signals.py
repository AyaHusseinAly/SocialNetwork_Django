from django.db.models.signals import post_save, pre_save, post_delete, pre_delete
from django.dispatch import receiver
from msgnotifications.models import Notification

from .models import Comment

@receiver(post_save, sender=Comment)
def after_comment_creation(sender,instance,created,*args,**kwargs):
    if created:
        text=str("comment from" + instance.owner.username+": "+instance.content[0:10])
        notify_instance = Notification.objects.create(sender=instance.owner, reciever=instance.post.owner,text=text)
        notify_instance.save()
    else:
        print("Updating..")


#  notification sender receiver text   // comment : post owner content
 #  
 # 
 # 
 # 
 # 
 # 
 # 
 # 
 # 
 #        