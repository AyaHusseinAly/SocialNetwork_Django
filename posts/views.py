from django.shortcuts import render , redirect
from django.http import HttpResponse
from .models import Post
from groups.models import Group
from .forms import PostForm
from django.contrib.auth.models import User
# from groups.models import Group
#from django.contrib.auth.decorators import login_required, permission_required
#@login_required
#@permission_required(["books.view_book"],raise_exception=True)
def index(request):
    query=request.GET.get('q','')
    if(query):
        first_name_query1=User.objects.filter(first_name__contains=str(query))
        first_name_query2=User.objects.filter(first_name__in=[query])
        last_name_query1=User.objects.filter(last_name__contains=str(query))
        last_name_query2=User.objects.filter(last_name__in=[query])
        users = first_name_query1.union(first_name_query1,last_name_query1,last_name_query2)
        return render(request,"users/index.html",{
            "usersResult":users,
            "query":query,
        })
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
        "groups":groups,
        "users":users

    })
    

def delete(request,id):
    post=Post.objects.get(pk=id)
    post.delete()
    return redirect("index")


def edit(request,id):
    postData=Post.objects.get(pk=id)
    post= PostForm(request.POST or None, instance=postData)
    if post.is_valid():
        post.save()
        return redirect("index")
    return render(request,"posts/edit.html",{'form':post, "data":postData})    

def view(request,id):
    post=Post.objects.get(pk=id)
    return render(request,"posts/view.html",{
        "post":post
    })
