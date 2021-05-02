
# Create your views here.
from django.shortcuts import render ,redirect
from django.contrib.auth import authenticate , login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from .forms import UserProfileForm



# Create your views here.
def index(request):
    query=request.GET.get('q','')
    if(query):
        first_name_query1=User.objects.filter(first_name__contains=str(query))
        first_name_query2=User.objects.filter(first_name__in=[query])
        last_name_query1=User.objects.filter(last_name__contains=str(query))
        last_name_query2=User.objects.filter(last_name__in=[query])
        users = first_name_query1.union(first_name_query1,last_name_query1,last_name_query2)
        return render(request,"searchResult.html",{
            "usersResult":users,
        })
    users=User.objects.all()

    return render(request,"searchResult.html",{
        
        "usersResult":users,

    })

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

def profile(request,id):
    user = User.objects.get(pk=id)
    return render(request,'profile.html',{
        "user":user,
    })