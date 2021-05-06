
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="group"),
    path("create", views.create, name="create"),
    path("leave/<int:id>", views.leave, name="leave"),
    path("listMembers/<int:id>", views.listMembers, name="listMembers"),
    path("invite/<int:id>", views.invite, name="invite"),
    path("request/<int:id>", views.request, name="group.request"),
    #     second try for acceptrequest::

    path("acceptrequest/<int:id>", views.acceptrequest,
         name="group.acceptrequest"),
    path("acceptRefuseRequest/<int:id>", views.acceptRefuseRequest,
         name="group.acceptRefuseRequest"),

    #
    path("show/<int:id>", views.show, name="show"),
    path("edit/<int:id>", views.edit, name="group.edit"),
    path("delete/<int:id>", views.delete, name="group.delete"),
    path("view/<int:id>", views.view, name="group.view"),
    path("sendrequest/<int:id>", views.groupRequest, name="group.sendrequest"),
    path("acceptInvitation/<int:id>", views.acceptInvitation,
         name="group.acceptInvitation"),
    path("sendRequestJoin/<int:id>", views.sendRequestJoin,
         name="group.sendRequestJoin"),
    path("cancelInvitation/<int:id>", views.cancelInvitation,
         name="group.cancelInvitation"),
     path('cancelRequestJoin/<int:id>',views.cancelRequestJoin,name='cancel-request-join')




]
