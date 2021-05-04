from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from groups.models import Group
# class UserCreateForm(UserCreationForm):
#     avatar = forms.CharField(required=True)
#     email= forms.CharField(required=True)

#     class Meta:
#         model = User
#         fields = ("username","email", "avatar", "password1", "password2")

#     def save(self, commit=True):
#         user = super(UserCreateForm, self).save(commit=False)
#         user.extra_field = self.cleaned_data["extra_field"]
#         if commit:
#             user.save()
#         return user

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=255)
    country = models.CharField(max_length=30, null=True, blank=True)
    avatar = models.ImageField(null=True, blank=True)
    birthdate = models.DateField(
        auto_now=False, auto_now_add=False, null=False, blank=False)
    about = models.TextField(max_length=500, null=True, blank=True)
    groups = models.ManyToManyField(Group, blank=True, null=True)
    # groups=models.ManyToManyField(Group,blank=True,null=True)
    # posts=models.ManyToManyField(Post,blank=True,null=True)

    def __str__(self):
        return self.user.username
