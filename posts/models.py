from django.db import models
from django.contrib.auth.models import User
from groups.models import Group


class Post(models.Model):
    content=models.CharField(max_length=2000)
    created_at=models.DateTimeField(auto_now_add=True)
    image=models.CharField(max_length=50,blank=True,null=True)
    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name="post")
    group=models.ForeignKey(Group,on_delete=models.CASCADE, null=True,blank=True,related_name="post")
    # likes=
    def __str__(self):
        return str(self.content[0:15]+"...")

class Comment(models.Model):
    content=models.CharField(max_length=1000)
    created_at=models.DateTimeField(auto_now_add=True)
    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name="comments")
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name="comments")
    def __str__(self):
        return str(self.content[0:15]+"...")






   
