from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Post , Comment , Like ,BadWord 
from groups.models import Group
from .forms import PostForm,PostEditForm
from .forms import CommentForm
from django.contrib.auth.models import User
from accounts.models import UserProfile
from django import forms
from friend.models import FriendList
from django.contrib.auth.decorators import login_required
from msgnotifications.models import Message, Notification 


def index(request):

    notifyCounter=len(  Notification.objects.filter(reciever=request.user).filter(read=False) )
    msgCounter=len(Message.objects.filter(reciever=request.user,read=False) )

    query = request.GET.get('q', '')
    if(query):
        first_name_query1 = User.objects.filter(userprofile__first_name__icontains=str(query))
        first_name_query2 = User.objects.filter(userprofile__first_name__in=[query])
        last_name_query1 = User.objects.filter(userprofile__last_name__icontains=str(query))
        last_name_query2 = User.objects.filter(userprofile__last_name__in=[query])
        username_query1 = User.objects.filter(username__in=[query])
        username_query2 = User.objects.filter(username__icontains=str(query))

        users = first_name_query1.union(
            first_name_query1, last_name_query1, last_name_query2,username_query1,username_query2)
        
        return render(request, "users/index.html", {
            "usersResult": users,
            "query": query,
        })
    try:
        posts=Post.objects.filter(owner=request.user)
    except:
        pass
    try:
        friend_list = FriendList.objects.get(user=request.user)
        for friend in friend_list.friends.all():
            posts=posts.union(Post.objects.filter(owner=friend))
    except FriendList.DoesNotExist:
        pass
    try:
        user_groups = request.user.userprofile.groups.all()
        for group in user_groups:
            posts=posts.union(Post.objects.filter(group=group))
    except:
        pass
    posts=posts.order_by('-created_at')
    groups=request.user.userprofile.groups.all()
    post=PostForm(request.POST, request.FILES or None)
    if post.is_valid():
        form_content=post.cleaned_data['content']
        form_image=None
        if 'image' in request.FILES:
            form_image = request.FILES['image']

        post_obj = Post.objects.create(
            content=form_content, owner=request.user, image=form_image)
        post_obj.save()
        return redirect("index")
    return render(request, "posts/index.html", {
        "form": post,
        "posts": posts,
        "groups": groups,
        "notifyCounter":notifyCounter,
        "msgCounter":msgCounter
        #  "post" : post

    })


def delete(request, id):
    post = Post.objects.get(pk=id)
    if request.user != post.owner:
        return render(request,'unauthorized.html')
    post.delete()
    return redirect("index")


def edit(request, id):
    postData = Post.objects.get(pk=id)
    if request.user != postData.owner:
        return render(request,'unauthorized.html')
    post = PostEditForm(request.POST or None, instance=postData)
    if post.is_valid():
        post.save()
        return redirect("index")
    return render(request, "posts/edit.html", {'form': post, "data": postData})


def view(request, id):
    post = Post.objects.get(pk=id)
    return render(request, "posts/view.html", {
        "post": post
    })


def AddCommentView(request, id):
    post = Post.objects.get(pk=id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        form_content = form.cleaned_data['content']
        comment_obj = Comment.objects.create(
            content=form_content, owner=request.user, post=post)
        comment_obj.save()
        return redirect("view", post.id)

    return render(request, "posts/add_comment.html", {
        "form": form,
        "post": post

    })

def delComment(request,id): 
    comment = Comment.objects.get(pk=id)
    if comment.owner != request.user:
        return render(request,'unauthorized.html')
    post=comment.post
    comment.delete()
    return redirect("/posts/view/"+str(post.id))

def like_post(request): 
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)

        if user in post_obj.liked.all():
            post_obj.liked.remove(user)
        else:
            post_obj.liked.add(user)  

        like, created = Like.objects.get_or_create(user = user,post_id = post_id ) 

        if not created:
            if like.value == 'Like':
                like.value = 'Unlike' 
            else :
                 like.value = 'Like'    
        like.save()            
        return redirect("index")

def post_likes(request, id):
    post = Post.objects.get(pk=id)
    return render(request, "posts/post_likes.html", {
        "post": post
    })    


