from django.shortcuts import render , redirect
from django.http import HttpResponse
import json
from django.contrib.auth.models import User
from django import forms


from accounts.models import UserProfile
from friend.models import FriendRequest

def friend_requests(request, *args, **kwargs):
    context = {}
    user = request.user
    if user.is_authenticated:
        user_id = kwargs.get("user_id")
        account =  User.objects.get(pk=user_id)
        if account == user:
            friend_requests = FriendRequest.objects.filter(receiver= account, is_active= True)
            context['friend_requests'] = friend_requests
        else:
            return HttpResponse("You can't view another users friend requests.")
    #else:
    #    redirect("login")
    return render(request, "friend/friend_requests.html", context)

def send_friend_request(request, *args, **kwargs):
    user = request.user #get authenticated user
    payload = {}
    if request.method == "POST" and user.is_authenticated:
        user_id = request.POST.get("receiver_user_id") #id of user who receive request
       #if user_id:
        receiver = User.objects.get(pk=user_id)
        friend_request = FriendRequest(sender=user, receiver= receiver)
        #try:
                # Get any friend requests (active and not-active)
        #    friend_requests = FriendRequest.objects.filter(sender=user, reciever= receiver)
                # find if any of them are active
        #        try:
        #            for request in friend_requests:
        #                if request.is_active:
        #                    raise Exception("You already sent them a friend request.")
                    # If none are active, then create a new friend request
        #            friend_request = FriendRequest(sender=user, receiver= receiver)
        #            friend_request.save()
        #            payload['response'] = "Friend request sent."
        #        except Exception as e:
         #            payload['response'] = str(e)
         #   except FriendRequest.DoesNotExist:
         #       # There are no friend request so create one.
         #       friend_request = FriendRequest(sender=user, receiver= receiver)
        friend_request.save()
         #       payload['response'] = "Friend request sent."
            
          #  if payload['response'] == None:
           #     payload['response'] = "something went wrong "
        #else:
        #    payload['response'] = "Unable to sent a friend request."
    else:
        payload['response'] = "You must be authenticated to send a friend request."
    return HttpResponse(json.dumps(payload), content_type="application/json")

def accept_friend_request(request, *args, **kwargs):
    user = request.user
    payload = {}
    if request.method == "GET" and user.is_authenticated:
        friend_request_id = kwargs.get("friend_request_id")
        if friend_request_id:
            friend_request = FriendRequest.objects.get(pk= friend_request_id)
            # confirm that is the correct request 
            if friend_request.receiver == user:
                if friend_request:
                    # found the request. Not accept it.
                    friend_request.accept()
                    payload['response'] = "Friend request accepted"
                else:
                    payload['response'] = "Something went wrong"
            else:
                payload['response'] = "That is not your request to accept."
        else:
            payload['response'] = "Unable to accept that friend request."
    return HttpResponse(json.dumps(payload), content_type="application/json")



