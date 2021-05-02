from django.shortcuts import render , redirect
from django.http import HttpResponse
from .models import Group
from itertools import chain

def index(request):
    query=request.GET.get('q','')
    if(query):
        groups = Group.objects.filter(name__contains=str(query)).union(Group.objects.filter(name__in=[query]))
    else:
        groups = Group.objects.all()

    return render(request,"groups/index.html",{
        
        "groups":groups

    })
