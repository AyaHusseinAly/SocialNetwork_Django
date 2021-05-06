from django.db import models
from django.contrib.auth.models import User
from groups.models import Group

import datetime





class Post(models.Model):
    content=models.TextField(max_length=2000 )
    created_at=models.DateTimeField(auto_now_add=True)
    image=models.ImageField(null=True, blank=True)
    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name="post")
    group=models.ForeignKey(Group,on_delete=models.CASCADE, null=True,blank=True,related_name="post")
    liked=models.ManyToManyField(User,default=None,blank=True,related_name="liked")
    def __str__(self):
        return str(self.content[0:15]+"...")

    @property
    def num_likes(self):
        self.liked.all().count()

class Comment(models.Model):

    content=models.TextField(max_length=1000 )
    created_at=datetime.datetime.now()

    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name="comments")
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name="comments")
    def __str__(self):
        return str(self.content[0:15]+"...")

LIKE_CHOICES = (
    ('Like','Like'),
    ('Unlike','Unlike')
)



class Like(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    value=models.CharField(choices=LIKE_CHOICES ,default='Like',max_length=10)
   
    def __str__(self):
        return str(self.post)
        
class BadWord(models.Model):

    word   = models.CharField(max_length=100)
    
    def __str__(self):
        return self.word


