from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.auth.models import User

def index(request):
    users= User.objects.exclude(id=request.user.id)

    return render(request,"friends/index.html",{
        "users":users
    })

# Create your views here.
