from django.contrib import admin
from django.urls import path ,include
from . import views

urlpatterns = [
    path("signup", views.signup,name="signup"),
    path('/logout_request/',views.logout_request,name='logout_request'),
    path("profile/<int:id>", views.profile,name="profile"),
    path("profile/<int:id>/about", views.about,name="about"),
    path("profile/<int:id>/edit",views.edit,name="editProfile"),

]