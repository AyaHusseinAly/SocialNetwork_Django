from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from msgnotifications.models import Message,Notification

from accounts.models import UserProfile
from friend.models import FriendRequest, FriendList


def friend_requests(request, *args, **kwargs):
    context = {}
    user = request.user

    user_id = kwargs.get("user_id")
    account = User.objects.get(pk=user_id)
    if account == user:
        friend_requests = FriendRequest.objects.filter(
            receiver=account, is_active=True)
        context['friend_requests'] = friend_requests
    else:
        return HttpResponse("You can't view another users friend requests.")
    return render(request, "friend/friend_requests.html", context)


def send_friend_request(request, *args, **kwargs):

    user = request.user  # get authenticated user

    payload = {}
    if request.method == "POST":
        user_id = request.POST.get("receiver_user_id") #id of user who receive request
       
        receiver = User.objects.get(pk=user_id)
        friend_request = FriendRequest(sender=user, receiver= receiver)
        friend_request.save()
    else:
        return render(request,'unauthorized.html')
    return HttpResponse(json.dumps(payload), content_type="application/json")


def accept_friend_request(request, *args, **kwargs):
    user = request.user
    payload = {}
    if request.method == "GET":
        friend_request_id = kwargs.get("friend_request_id")
        friend_request = FriendRequest.objects.get(pk= friend_request_id)
        friend_request.accept()
        payload['response'] = "Friend request accepted."
    else:
        return render(request,'unauthorized.html')
    return HttpResponse(json.dumps(payload), content_type="application/json")



def decline_friend_request(request, *args, **kwargs):
    user = request.user
    payload = {}
    if request.method == "GET":
        friend_request_id = kwargs.get("friend_request_id")
        if friend_request_id:
            friend_request = FriendRequest.objects.get(pk=friend_request_id)
            if friend_request.receiver == user:  # checking that the request is mine to decline
                if friend_request:
                # found request then decline it
                    friend_request.decline()
                    payload['response'] = "Friend request declined."
                else:
                    payload['response'] = "Something went wrong."
            else:
                payload['response'] = "That is not your friend request to decline"
        else:
            payload['response'] = "Unable to decline that friend request."
    else:
        return render(request,'unauthorized.html')
    return HttpResponse(json.dumps(payload), content_type="application/json")


def remove_friend(request, *args, **kwargs):
    user = request.user
    payload = {}
    if request.method == "POST":
        user_id = request.POST.get("reciever_user_id")
        if user_id:
            try:
                removee = User.objects.get(pk=user_id)
                friend_list = FriendList.objects.get(user=user)
                friend_list.unfriend(removee)
                payload['response'] = "Friend Removed."
            except Exception as e:
                payload['response'] = f"something went wronghu: {str(e)}"
        else:
            payload['response'] = "Unable to remove that friend"
    else:
        return render(request,'unauthorized.html')
    return HttpResponse(json.dumps(payload), content_type="application/json")


def cancel_friend_request(request, *args, **kwargs):
    user = request.user
    payload= {}
    if request.method == "POST" :
        user_id = request.POST.get("receiver_user_id")
        if user_id:
            receiver = User.objects.get(pk=user_id)
            try:
                friend_requests = FriendRequest.objects.filter(sender=user, receiver= receiver, is_active=True)
            except Exception as e:
                payload['response'] = "Nothing to cancel. Friend request does not exist."

            # There should only ever be a single active friend request at any given time
            # Cancel them all just in case.
            if len(friend_requests) > 1:
                for request in friend_requests:
                    request.cancel()
                payload['response'] = "Friend request cancelled."
            else:
                # found the request. Now cancel it.
                friend_requests.first().cancel()
                payload['response'] = "Friend request cancelled."
        else:
            payload['response'] = "Unable to cancel that friend request."
    else:
        return render(request,'unauthorized.html')

    return HttpResponse(json.dumps(payload), content_type="application/json")

 
def friend_list_view1(request, *args, **kwargs):
    context = {}
    user = request.user
    try:
        friend_list = FriendList.objects.get(user=user)
    except FriendList.DoesNotExist:
        return render(request, "friend_list.html", context)
    friends = []  
    for friend in friend_list.friends.all():
        friends.append((friend))

    context['friends'] = friends
    notifyCounter=len(  Notification.objects.filter(reciever=request.user).filter(read=False) )
    context['notifyCounter']=notifyCounter
    friend_requests = FriendRequest.objects.filter(receiver=user, is_active=True)
    context["checker"]={"friend_requests":friend_requests}
    return render(request, "friend_list.html", context)
