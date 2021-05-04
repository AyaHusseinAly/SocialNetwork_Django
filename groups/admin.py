from django.contrib import admin
from .models import Group,GroupInvite

# Register your models here.
admin.site.register(Group)
admin.site.register(GroupInvite)

