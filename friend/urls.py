from django.urls import path

from friend.views import (
    send_friend_request,
    friend_requests,
    accept_friend_request,
    decline_friend_request,
    cancel_friend_request,
)

app_name = "friend"

urlpatterns = [
    path('friend_request/', send_friend_request, name="friend-request"),
    path('friend_request/<user_id>/', friend_requests, name="friend-requests"),
    path('accept_friend_request/<friend_request_id>/', accept_friend_request, name="friend-request-accept"),
    path('decline_friend_request/<friend_request_id>', decline_friend_request, name="friend-request-decline"),
    path('friend_request_cancel/', cancel_friend_request, name="friend-request-cancel"),

]