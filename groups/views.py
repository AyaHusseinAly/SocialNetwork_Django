from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Group
from itertools import chain
from .forms import GroupForm


def index(request):
    query = request.GET.get('q', '')
    if(query):
        groups = Group.objects.filter(name__contains=str(query)).union(
            Group.objects.filter(name__in=[query]))
    else:
        groups = Group.objects.all()

    return render(request, "groups/index.html", {

        "groups": groups

    })


def create(request):
    # request.POST or None means ==>take request form if get it or do nothing
    form = GroupForm(request.POST or None)
    if form.is_valid():
        form.save()  # means send it to model and save it
        return redirect("group")
    return render(request, "groups/create.html", {
        "form": form
    })
