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


def edit(request,id):
    bookData=Book.objects.get(pk=id)
    book= BookForm(request.POST or None, instance=bookData)
    if book.is_valid():
        book.save()
        return redirect("index")
    return render(request,"books/edit.html",{'form':book, "data":bookData})    

def delete(request,id):
    post=Post.objects.get(pk=id)
    post.delete()
    return redirect("index")

def view(request,id):
    book=Book.objects.get(pk=id)
    return render(request,"books/view.html",{
        "book":book
    })

