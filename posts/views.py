from django.shortcuts import render , redirect
from django.http import HttpResponse
from .models import Post , Comment
from groups.models import Group
from .forms import PostForm 
from .forms import CommentForm
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django import forms


# from django.views.generic import CreateView
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
        username_query=User.objects.filter(username__in=[query])
        users = first_name_query1.union(first_name_query1,last_name_query1,last_name_query2,username_query)
        return render(request,"users/index.html",{
            "usersResult":users,
            "query":query,
        })
    posts= Post.objects.all()
    groups= Group.objects.all()
    post= PostForm(request.POST, request.FILES or None)
    if post.is_valid():
        form_content=post.cleaned_data['content']
        if request.FILES['image']:
            form_image = request.FILES['image']
        else:
            form_image=None
        #fs = FileSystemStorage()
        #filename = fs.save(form_image.name,form_image)
        #uploaded_file_url = fs.url(filename)
        post_obj=Post.objects.create( content=form_content,owner=request.user,image=form_image)
        post_obj.save()
        return redirect("index")
    return render(request,"posts/index.html",{
        "posts":posts,
        "groups":groups

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

# class AddCommentView(CreateView):
#     model = Comment
#     template_name = "add_comment.html"
#     fields = ("content",)    

def AddCommentView(request,id):
    post = Post.objects.get(pk=id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        
        form_content=form.cleaned_data['content']
        comment_obj=Comment.objects.create( content=form_content,owner=request.user,post=post)
        comment_obj.save()
        # form.save()
        return redirect("view",post.id)

    return render(request,"posts/add_comment.html",{
            "form": form,
             "post": post
            
        })

def delComment(request,id): 
    
    comment = Comment.objects.get(pk=id)
    comment.delete()
    return redirect("index")