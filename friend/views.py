from django.shortcuts import render
from django.http import HttpResponse
import json
from django.contrib.auth.models import User


from accounts.models import UserProfile
from friend.models import FriendRequest

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

def decline_friend_request(request,*args,**kwargs):
    user=request.user
    payload={}
    if request.method == 'GET' and user.is_authenticated:
        friend_request_id=kwargs.get("friend_request_id")
        if friend_request_id:
            friend_request=FriendRequest.objects.get(pk=friend_request_id)
            if friend_request:
                if friend_request.receiver == user : #checking that the request is mine to decline
                    friend_request.decline()
                    payload['response']= "Request Declined."
                else:
                    payload['response']="Not your request to decline."
            else:
                payload['response']="something went wrong."
        else:
            payload['response']="unable to decline that request"
    else:
        payload['response']="please log in to decline"
    return HttpResponse(json.dumps(payload), content_type="application/json")

                