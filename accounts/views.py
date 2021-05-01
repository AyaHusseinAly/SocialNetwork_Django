
# Create your views here.
from django.shortcuts import render ,redirect
from django.contrib.auth import authenticate , login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from .forms import UserProfileForm


# Create your views here.

def signup(request):
    form = UserCreationForm(request.POST or None) 
    profile_form = UserProfileForm(request.POST or None)

    if form.is_valid() and profile_form.is_valid():
            form.save()

            profile = profile_form.save(commit = False)
          
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username , password=password)
            profile.user = user
            profile.save()
            if user:
                login(request , user)
                return redirect("/admin/")
            
    context = {'profile_form' : profile_form ,'form' : form }
    return render(request , "registration/signup.html", context)

def profile(request):
    return HttpResponseNotFound('<h1>profile</h1>')