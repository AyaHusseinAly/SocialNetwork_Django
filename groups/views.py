from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from .models import Group
from itertools import chain
from .forms import GroupForm
from posts.models import Post
from groups.models import Group, GroupInvite, GroupRequestJoin
from msgnotifications.models import Notification
from posts.forms import PostForm
from accounts.models import UserProfile
from django.contrib.auth.models import User


def index(request):
    query = request.GET.get('q', '')
    if(query):
        groups = Group.objects.filter(name__icontains=str(query)).union(
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
        request.user.userprofile.groups.add(group)
        # form.save()  # means send it to model and save it
        # return redirect("group")
        return redirect("/groups/show/"+str(group.id))
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
    posts = Post.objects.filter(group=group).order_by('-created_at')

    groups = Group.objects.all()
    users_in_group = UserProfile.objects.filter(Q(groups=id))

    invited = GroupInvite.objects.filter(
        inviteTo=request.user).filter(group=group)

    members = []
    for user in users_in_group:
        members.append(user.user)
    # print(users_in_group)
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
        "users_in_group": members,
        "invited": invited

    })


def delete(request, id):
    post = Post.objects.get(pk=id)
    if request.user != post.owner:
        return render(request,'unauthorized.html')
    post.delete()
    return redirect("/groups/show/"+str(post.group.id))


def edit(request, id):
    postData = Post.objects.get(pk=id)
    if request.user != postData.owner:
        return render(request,'unauthorized.html')
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

    users = UserProfile.objects.filter(~Q(groups=id))
    # print(users[0].user.id)
    # print(users[0].first_name)
    group = Group.objects.get(id=id)
    alreadyInvitedUsers = GroupInvite.objects.filter(group=group)
    print(alreadyInvitedUsers)
    notMember = []
    # for user in users:
    #     print(user.user)
    #     notMember.append(user.user.id)
    notInvited = False
    for user in users:
        for alreadyInvitedUser in alreadyInvitedUsers:
            # print("already invited "+alreadyInvitedUser.inviteTo.username)
            if user.user == alreadyInvitedUser.inviteTo:
                # print("****entered equal "+user.user.username +
                #       "===="+alreadyInvitedUser.inviteTo.username)
                notInvited = True
        if notInvited == False:
            notMember.append(user.user.id)
        notInvited = False
        # print("users not in group "+user.user.username)

    invites = User.objects.filter(id__in=notMember)
    return render(request, "groups/invite.html", {
        "invites": invites,
        "id": id,
        "alreadyInvitedUsers": alreadyInvitedUsers
    })


def groupRequest(request, id):
    # print(dict(request.POST)["groupRequest"])
    group = Group.objects.get(id=id)
    if request.POST:
        for user_id in dict(request.POST)["groupRequest"]:
            user = User.objects.get(id=user_id)
            # UserProfile.objects.get(user=user)
            invite = GroupInvite.objects.create(
                inviteFrom=request.user, inviteTo=user, group=group)
            invite.save()

    return redirect("/groups/invite/"+str(group.id))
    # return redirect("/groups/show/"+str(group.id))


def acceptInvitation(request, id):
    profile = UserProfile.objects.get(user=request.user)
    group = Group.objects.get(id=id)
    profile.groups.add(group)
    invitedGroup = GroupInvite.objects.get(inviteTo=request.user, group=group)
    invitedGroup.delete()
    return redirect("/groups/show/"+str(group.id))


def cancelInvitation(request, id):
    group = Group.objects.get(id=id)
    invitedGroup = GroupInvite.objects.get(inviteTo=request.user, group=group)
    invitedGroup.delete()
    return redirect("/groups/show/"+str(group.id))


def sendRequestJoin(request, id):
    group = Group.objects.get(id=id)

    try:
        GroupRequestJoin.objects.get(
            requestFrom=request.user, requestTo=group.owner, group=group)
        return HttpResponse("You Aleardy send request join.")
    except:
        invite = GroupRequestJoin.objects.create(
            requestFrom=request.user, requestTo=group.owner, group=group)
        invite.save()
    # return redirect("/groups/show/"+str(group.id))
    return redirect("group")


# def request(request, id):
#     group = Group.objects.get(id=id)
#     requests = GroupRequestJoin.objects.filter(
#         requestTo=request.user).filter(group=group)
#     return render(request, "groups/request.html", {
#         "requests": requests,
#         "id": id
#     })
def request(request, id):
    group = Group.objects.get(id=id)
    requests = GroupRequestJoin.objects.filter(
        requestTo=request.user).filter(group=group)
    return render(request, "groups/groupRequests.html", {
        "requests": requests,
        "id": id
    })
    # print(requests)
    # return redirect('group')


def acceptrequest(request, id):
    group = Group.objects.get(id=id)
    text = " you are now a member in " + \
        str(group.name+" group")
    for user_id in dict(request.POST)["groupRequest"]:
        user = User.objects.get(id=user_id)
        user.userprofile.groups.add(group)
        notify_instance = Notification.objects.create(
            sender=group.owner, reciever=user, text=text, notifyType="groupView", instance_id=group.id)
        notify_instance.save()

    return redirect("group")


def acceptRefuseRequest(request, id):
    group = Group.objects.get(id=id)
    user_id = request.POST['user']
    user = User.objects.get(id=int(user_id))
    print("print1111111111111")
    print(user)
    print(request.POST['submit'])
    print(dict(request.POST)['submit'] == ['Accept'])
    if dict(request.POST)['submit'] == ['Accept']:
        user.userprofile.groups.add(group)
        text = " you are now a member in " + str(group.name+" group")
        notify_instance = Notification.objects.create(
            sender=group.owner, reciever=user, text=text, notifyType="groupView", instance_id=group.id)
        notify_instance.save()
    elif dict(request.POST)['submit'] == ['Refuse']:
        text = " Admin of " + str(group.name+" group refused your request")
        notify_instance = Notification.objects.create(
            sender=group.owner, reciever=user, text=text, notifyType="groupView", instance_id=group.id)
        notify_instance.save()
    request = GroupRequestJoin.objects.get(
        requestTo=request.user, group=group)
    request.delete()
    return redirect("group")


def leave(request, id):
    group = Group.objects.get(id=id)
    request.user.userprofile.groups.remove(group)
    if request.user == group.owner:
        group.delete()
        # return redirect("group")

    return redirect("group")
    # return redirect("/groups/show/"+str(group.id))


def listMembers(request, id):
    group = Group.objects.get(id=id)
    users = User.objects.filter(Q(userprofile__groups=group))
    print(users)

    return render(request, "groups/members.html", {
        "users": users,
        "group": group
    })
