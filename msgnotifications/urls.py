
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index,name="msgPage"),
    path("delete/<int:id>", views.delete,name="msgDelete"),

]