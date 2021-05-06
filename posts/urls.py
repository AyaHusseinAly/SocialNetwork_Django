
from django.urls import path
from .import views


urlpatterns = [
    path("", views.index,name="index"),
    path("edit/<int:id>", views.edit,name="edit"),
    path("delete/<int:id>", views.delete,name="delete"),
    path("view/<int:id>", views.view,name="view"),
    path("view/<int:id>/comment",views.AddCommentView,name="add_comment"),
    path("comment/<int:id>",views.delComment,name="del_comment"),
    path("like/",views.like_post,name="like-post"),
    path('view/<int:id>/postlikes/', views.post_likes, name='post-likes'),
    
]
