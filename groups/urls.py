
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="group"),
    path("create", views.create, name="create"),

]
