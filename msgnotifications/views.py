from django.shortcuts import render , redirect
from django.urls import reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import Message, Notification
from .forms import MsgForm
from django.contrib.auth.models import User
from accounts.models import  UserProfile
from friend.models import FriendList


def index(request):
    friendId=int(request.GET.get('id',request.user.id))
    query=request.GET.get('q','')
    if(query):
        first_name_query1=User.objects.filter(first_name__contains=str(query))
        first_name_query2=User.objects.filter(first_name__in=[query])
        last_name_query1=User.objects.filter(last_name__contains=str(query))
        last_name_query2=User.objects.filter(last_name__in=[query])
        users = first_name_query1.union(first_name_query1,last_name_query1,last_name_query2)
        return render(request,"users/index.html",{
            "usersResult":users,
            "query":query,
        })
    
    flag = 0 # check to see if friendID doesn't exist in my friend list
    
    try:
        friend_list = FriendList.objects.get(user=request.user)
    except FriendList.DoesNotExist:
        return render(request, "friend/friend_list.html")
    friends = [] 
    for friend in friend_list.friends.all():
        friends.append((friend))
        if friendId == friend.id:
            flag=1
    if friendId==request.user.id:
        flag=1
    if flag == 0:
        return redirect('/profile/'+str(friendId))
    usersforAvatar  = UserProfile.objects.filter(user__in=friends)   
    sender1=User.objects.get(pk=friendId)
    sender2= User.objects.get(username=request.user.username)
    reciever1= User.objects.get(pk=friendId)
    reciever2=User.objects.get(username=request.user.username)
    messages= Message.objects.filter(reciever=reciever1,sender=sender2) |Message.objects.filter(reciever=reciever2,sender=sender1) 
    msg= MsgForm(request.POST or None)
    if msg.is_valid():
        form_text=msg.cleaned_data['text']
        msg_obj=Message.objects.create( text=form_text,sender=request.user,reciever=reciever1)
        msg_obj.save()
        return HttpResponseRedirect(request.path_info+"?id="+str(friendId))
    return render(request,"index.html",{
        "friends":friends,
        "messages":messages,
        "msgto":sender1.username,
        "avatars":usersforAvatar
    })
    

################################################## Notififcations #####################################################################    
def notify(request):

    notifications= Notification.objects.filter(reciever=request.user).order_by('-created_at')
    return render(request,"notificationIndex.html",{
        "notifications":notifications
    })