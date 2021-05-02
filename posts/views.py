from django.shortcuts import render , redirect
from django.http import HttpResponse
from .models import Post
from django.contrib.auth.models import User
# from groups.models import Group
#from django.contrib.auth.decorators import login_required, permission_required


#@login_required
#@permission_required(["books.view_book"],raise_exception=True)
def index(request):
    posts= Post.objects.all()
    query=request.GET.get('q','')
    if(query):
        first_name_query1=User.objects.filter(first_name__contains=str(query))
        first_name_query2=User.objects.filter(first_name__in=[query])
        last_name_query1=User.objects.filter(last_name__contains=str(query))
        last_name_query2=User.objects.filter(last_name__in=[query])
        users = first_name_query1.union(first_name_query1,last_name_query1,last_name_query2)
        return render(request,"users/index.html",{
        "users":users,
        })
    else:
        posts = Post.objects.all()
        return render(request,"posts/index.html",{
        "posts":posts,
        # "groups":groups

        })
    # groups= Group.objects.all()

    
