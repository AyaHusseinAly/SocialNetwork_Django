from django.contrib import admin
from .models import UserProfile
from django.contrib.auth.models  import User
from .forms import UserProfileForm
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin


# Register your models here.
class UserProfileInline(admin.StackedInline):
    model=UserProfile
    max_num=1
class UserAdmin(AuthUserAdmin):
    inlines=[UserProfileInline]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
