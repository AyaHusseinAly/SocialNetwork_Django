from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from .models import Group
from itertools import chain
from .forms import GroupForm
from posts.models import Post
from groups.models import Group, GroupInvite
from posts.forms import PostForm
from accounts.models import UserProfile
from django.contrib.auth.models import User


def index(request):
    query = request.GET.get('q', '')
    if(query):
        groups = Group.objects.filter(name__contains=str(query)).union(
            Group.objects.filter(name__in=[query]))
    else:
        groups = Group.objects.all()

    return render(request, "groups/index.html", {

        "groups": groups

    })


def create(request):
    # request.POST or None means ==>take request form if get it or do nothing
    form = GroupForm(request.POST, request.FILES or None)
    if form.is_valid():
        print(form)
        name = form.cleaned_data['name']
        privacy = form.cleaned_data['privacy']
        description = form.cleaned_data['description']
        cover = form.cleaned_data['cover']
        group = Group.objects.create(
            name=name, privacy=privacy, description=description, cover=cover, owner=request.user)
        # form.save()  # means send it to model and save it
        return redirect("group")
    return render(request, "groups/create.html", {
        "form": form
    })


def show(request, id):
    group = Group.objects.get(id=id)
    query = request.GET.get('q', '')
    if(query):
        first_name_query1 = User.objects.filter(
            first_name__contains=str(query))
        first_name_query2 = User.objects.filter(first_name__in=[query])
        last_name_query1 = User.objects.filter(last_name__contains=str(query))
        last_name_query2 = User.objects.filter(last_name__in=[query])
        users = first_name_query1.union(
            first_name_query1, last_name_query1, last_name_query2)
        return render(request, "users/index.html", {
            "usersResult": users,
            "query": query,
        })
    posts = Post.objects.filter(group=group)
    groups = Group.objects.all()
    # accounts = UserProfile.objects.all()
    post = PostForm(request.POST or None)
    if post.is_valid():
        form_content = post.cleaned_data['content']
        post_obj = Post.objects.create(
            content=form_content, owner=request.user, group=group)
        post_obj.save()
        return redirect("/groups/show/"+str(group.id))
    return render(request, "groups/show.html", {
        "posts": posts,
        "groups": groups,
        "group": group,

    })


def delete(request, id):
    post = Post.objects.get(pk=id)
    post.delete()
    return redirect("/groups/show/"+str(post.group.id))


def edit(request, id):
    postData = Post.objects.get(pk=id)
    post = PostForm(request.POST or None, instance=postData)

    if post.is_valid():
        post.save()
        return redirect("/groups/show/"+str(postData.group.id))
    return render(request, "group-posts/edit.html", {'form': post, "data": postData})


def view(request, id):
    post = Post.objects.get(pk=id)
    return render(request, "group-posts/view.html", {
        "post": post
    })


def invite(request, id):
    # friends = Group.objects.filter(id=id)[0].members.values_list()
    # # print(friends[0].members)
    # print(len(friends))
    # query = UserProfile.objects
    # inviteUsers = UserProfile.objects.filter(~Q(id=friends[0][0]))
    # print(query)
    users = UserProfile.objects.filter(~Q(groups=id))
    print(users[0].user.id)
    print(users[0].first_name)
#     names_to_exclude = [users for o in objects_to_exclude]
# Foo.objects.exclude(name__in=names_to_exclude)
    # invites = User.objects.filter(id=users.user).exclude(id=request.user.id)
    notMember = []
    for user in users:
        notMember.append(user.user.id)
    invites = User.objects.filter(id__in=notMember)
    # friends =UserProfile.objects.filter()
    # print(invites)
    return render(request, "groups/invite.html", {
        "invites": invites,
        "id": id
    })


def groupRequest(request, id):
    # print(dict(request.POST)["groupRequest"])
    group = Group.objects.get(id=id)
    for user_id in dict(request.POST)["groupRequest"]:
        user = User.objects.get(id=user_id)
        # UserProfile.objects.get(user=user)
        invite = GroupInvite.objects.create(
            inviteFrom=request.user, inviteTo=user, group=group)
        invite.save()

    return redirect("group")
