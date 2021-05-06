from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Post , Comment , Like ,BadWord 
from groups.models import Group
from .forms import PostForm,PostEditForm
from .forms import CommentForm
from django.contrib.auth.models import User
from accounts.models import UserProfile
from django import forms


# from django.views.generic import CreateView
# from groups.models import Group
#from django.contrib.auth.decorators import login_required, permission_required

#@login_required
#@permission_required(["books.view_book"],raise_exception=True)

def index(request):
    
    query = request.GET.get('q', '')
    if(query):
        first_name_query1 = User.objects.filter(userprofile__first_name__contains=str(query))
        first_name_query2 = User.objects.filter(userprofile__first_name__in=[query])
        last_name_query1 = User.objects.filter(userprofile__last_name__contains=str(query))
        last_name_query2 = User.objects.filter(userprofile__last_name__in=[query])
        username_query = User.objects.filter(username__in=[query])
        users = first_name_query1.union(
            first_name_query1, last_name_query1, last_name_query2,username_query)
        
        return render(request, "users/index.html", {
            "usersResult": users,
           
            "query": query,
        })

    posts = Post.objects.all()
    groups = Group.objects.all()
    post = PostForm(request.POST, request.FILES or None)

    if post.is_valid():
        form_content=post.cleaned_data['content']
        form_image=None
        if 'image' in request.FILES:
            form_image = request.FILES['image']

        post_obj = Post.objects.create(
            content=form_content, owner=request.user, image=form_image)
        post_obj.save()
        return redirect("index")
    # else:
       
        # print(post.errors)
        #  post = PostForm()
        #  args['post'] = post
        
       
    return render(request, "posts/index.html", {
        "posts": posts,
        "groups": groups,
        #  "post" : post
    })


def delete(request, id):
    post = Post.objects.get(pk=id)
    post.delete()
    return redirect("index")


def edit(request, id):
    postData = Post.objects.get(pk=id)
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

# class AddCommentView(CreateView):
#     model = Comment
#     template_name = "add_comment.html"
#     fields = ("content",)


def AddCommentView(request, id):
    post = Post.objects.get(pk=id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        form_content = form.cleaned_data['content']
        comment_obj = Comment.objects.create(
            content=form_content, owner=request.user, post=post)
        comment_obj.save()
        # form.save()
        return redirect("view", post.id)

    return render(request, "posts/add_comment.html", {
        "form": form,
        "post": post

    })

def delComment(request,id): 
    # post = Post.objects.get(pk=id)
    comment = Comment.objects.get(pk=id)
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

# def post_likes(request, id):
#     post = post = Post.objects.get(pk=id)
#     post_likes = post.liked.all()
#     context = {'post_likes': post_likes,}

#     return render(request, 'posts/post_likes.html', context)

def post_likes(request, id):
    post = Post.objects.get(pk=id)
    return render(request, "posts/post_likes.html", {
        "post": post
    })    

