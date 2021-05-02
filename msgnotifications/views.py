from django.shortcuts import render , redirect
from django.urls import reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
#from .models import Friends
from .models import Message
from .forms import MsgForm
from django.contrib.auth.models import User
#from django.contrib.auth.decorators import login_required, permission_required


#@login_required
#@permission_required(["books.view_book"],raise_exception=True)
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
    #friends= Friends.objects.all()
    
    #friends=[{'id':1,'name':"Amal Tamam",'img':"exPP3.png"},{'id':2,'name':"Alaa Hesham",'img':"alaa.png"},{'id':3,'name':"Eman Hussein",'img':"eman.png"},{'id':4,'name':"Fatma Tarek",'img':"fatma.png"}]
    sender1=User.objects.get(pk=friendId)
    sender2= User.objects.get(username=request.user.username)
    reciever1= User.objects.get(pk=friendId)
    reciever2=User.objects.get(username=request.user.username)
    messages= Message.objects.filter(reciever=reciever1,sender=sender2) |Message.objects.filter(reciever=reciever2,sender=sender1) 
    friends=User.objects.exclude(username=request.user.username)
    msg= MsgForm(request.POST or None)
    if msg.is_valid():
        form_text=msg.cleaned_data['text']
        msg_obj=Message.objects.create( text=form_text,sender=request.user,reciever=reciever1)
        msg_obj.save()
        #return redirect("msgPage",id=friendId)
        #return redirect(reverse('msgPage', kwargs={"id": friendId}))
        return HttpResponseRedirect(request.path_info+"?id="+str(friendId))

    return render(request,"index.html",{
        "friends":friends,
        "messages":messages

    })
    

def delete(request,id):
    msg=Message.objects.get(pk=id)
    msg.delete()
    return redirect("index")
