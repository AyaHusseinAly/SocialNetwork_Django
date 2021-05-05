
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="group"),
    path("create", views.create, name="create"),
    path("invite/<int:id>", views.invite, name="invite"),
    path("show/<int:id>", views.show, name="show"),
    path("edit/<int:id>", views.edit, name="group.edit"),
    path("delete/<int:id>", views.delete, name="group.delete"),
    path("view/<int:id>", views.view, name="group.view"),
    path("sendrequest/<int:id>", views.groupRequest, name="group.sendrequest"),


]
