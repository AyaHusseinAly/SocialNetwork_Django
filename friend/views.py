from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


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
    if request.method == "POST" and user.is_authenticated:
        # id of user who receive request
        user_id = request.POST.get("receiver_user_id")
       # if user_id:
        receiver = User.objects.get(pk=user_id)
        friend_request = FriendRequest(sender=user, receiver=receiver)
        # try:
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
        # else:
        #    payload['response'] = "Unable to sent a friend request."
    else:
        payload['response'] = "You must be authenticated to send a friend request."
    return HttpResponse(json.dumps(payload), content_type="application/json")


def accept_friend_request(request, *args, **kwargs):
    user = request.user
    payload = {}
    if request.method == "GET" and user.is_authenticated:
        friend_request_id = kwargs.get("friend_request_id")
        # if friend_request_id:
        friend_request = FriendRequest.objects.get(pk=friend_request_id)
        # confirm that is the correct request
        # if friend_request.receiver == user:
        # if friend_request:
        # found the request. Not accept it.
        friend_request.accept()
        payload['response'] = "Friend request accepted."
        # else:
        #         payload['response'] = "Something went wrong"
        # else:
        #     payload['response'] = "That is not your request to accept."
        # else:
        #     payload['response'] = "Unable to accept that friend request."
    return HttpResponse(json.dumps(payload), content_type="application/json")


def decline_friend_request(request, *args, **kwargs):
    user = request.user
    payload = {}
    if request.method == "GET" and user.is_authenticated:
        friend_request_id = kwargs.get("friend_request_id")
        if friend_request_id:
            friend_request = FriendRequest.objects.get(pk=friend_request_id)
        # if not friend_request.DoesNotExist:
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
        payload['response'] = "You must be authenticated to decline a friend request."
    return HttpResponse(json.dumps(payload), content_type="application/json")


def remove_friend(request, *args, **kwargs):
    user = request.user
    payload = {}
    if request.method == "POST" and user.is_authenticated:
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
        payload['response'] = "You must be signed in"
    return HttpResponse(json.dumps(payload), content_type="application/json")


def cancel_friend_request(request, *args, **kwargs):
    user = request.user
    payload = {}
    if request.method == "POST" and user.is_authenticated:
        user_id = request.POST.get("receiver_user_id")
        if user_id:
            receiver = User.objects.get(pk=user_id)
            try:
                friend_requests = FriendRequest.objects.filter(
                    sender=user, receiver=receiver, is_active=True)
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
        payload['response'] = "You must be authenticated to cancel a friend request."
    return HttpResponse(json.dumps(payload), content_type="application/json")

# def friend_list_view(request, *args, **kwargs):
#     context = {}
#     user = request.user
#     if user.is_authenticated:
#         user_id = kwargs.get("user.id")
#         if user_id:
#             try:
#                 this_user = User.objects.get(pk=user_id)
#                 context['this_user'] = this_user
#             except User.DoesNotExist:
#                 return HttpResponse("That user does not exist.")
#             try:
#                 friend_list = FriendList.objects.get(user=this_user)
#             except FriendList.DoesNotExist:
#                 return HttpResponse("could not find a friends list for {this_user.username}")

#              # Must be friends to view a friends list
#             if user != this_user:
#                 if not user in friend_list.friends.all():
#                     return HttpResponse("You must be friends to view their friends list")

#             friends = [] #[(account1, True), (account1, False), ... ]
#             auth_user_friend_list = FriendList.objects.get(user=user)
#             for friend in friend_list.friends.all():
#                 friends.append((friend, auth_user_friend_list.is_mutual_friend(friend)))
#             context['friends'] = friends
#         else:
#             return HttpResponse("You must be friends to view their fiends list.")
#         return render(request, "friend/friend_list.html", context)

# def friend_list_view1(request, *args, **kwargs):
#     context = {}
#     user = request.user
#     #if user.is_authenticated:
#     try:
#         friend_list = FriendList.objects.get(user=user)
#     except FriendList.DoesNotExist:
#         return HttpResponse("could not find a friends list for {this_user.username}")
#     friends = [] #[(account1, True), (account1, False), ... ]
#     auth_user_friend_list = FriendList.objects.get(user=user)
#     for friend in friend_list.friends.all():
#         friends.append((friend, auth_user_friend_list.is_mutual_friend(friend)))

#     context['friends'] = friends
#     return render(request, "friend_list.html", context)
#     #return HttpResponse("You must be friends to view their friends list")


def friend_list_view1(request, *args, **kwargs):
    context = {}
    user = request.user
    #context['friends'] = null
    # if user.is_authenticated:
    try:
        friend_list = FriendList.objects.get(user=user)
    except FriendList.DoesNotExist:
        # return HttpResponse("could not find a friends list for {this_user.username}")
        return render(request, "friend_list.html", context)
    friends = []  # [(account1, True), (account1, False), ... ]
    # auth_user_friend_list = FriendList.objects.get(user=user)
    for friend in friend_list.friends.all():
        # friends.append((friend, auth_user_friend_list.is_mutual_friend(friend)))
        friends.append((friend))

    context['friends'] = friends
    return render(request, "friend_list.html", context)
    # return HttpResponse("You must be friends to view their friends list")
