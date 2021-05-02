from django.shortcuts import render , redirect
from django.http import HttpResponse
from .models import Post
from groups.models import Group
from django.contrib.auth.models import User
#from django.contrib.auth.decorators import login_required, permission_required


#@login_required
#@permission_required(["books.view_book"],raise_exception=True)
def index(request):
    posts= Post.objects.all()
    groups= Group.objects.all()
    users= User.objects.all()

    return render(request,"posts/index.html",{
        "posts":posts,
        "groups":groups,
        "users":users

    })
