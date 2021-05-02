from django.shortcuts import render , redirect
from django.http import HttpResponse
from .models import Post
from groups.models import Group
from .forms import PostForm

#from django.contrib.auth.decorators import login_required, permission_required


#@login_required
#@permission_required(["books.view_book"],raise_exception=True)
def index(request):
    posts= Post.objects.all()
    groups= Group.objects.all()
    post= PostForm(request.POST or None)
    if post.is_valid():
        form_content=post.cleaned_data['content']
        post_obj=Post.objects.create( content=form_content,owner=request.user)
        post_obj.save()
        return redirect("index")
    return render(request,"posts/index.html",{
        "posts":posts,
        "groups":groups

    })

