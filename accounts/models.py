from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

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
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    location = models.CharField(max_length=30)
    age = models.IntegerField()

    def __str__(self):
        return self.user.username
