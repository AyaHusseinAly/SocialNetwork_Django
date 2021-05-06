"""bookstore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin

from django.conf.urls.static import static
from django.conf.urls import url
from django.conf import settings
from django.urls import path, include
from django.views.generic import TemplateView,RedirectView
from posts import views

urlpatterns = [
    path("", views.index,name='home'),
    path("", include("accounts.urls")),
    path("", include("django.contrib.auth.urls")),
    path('admin/', admin.site.urls),
    path('friend/',include("friend.urls")),

    path('posts/', include("posts.urls")),
    path('groups/', include("groups.urls")),
    path('messages/', include("msgnotifications.urls")), #route for messages and notifications

]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
urlpatterns += [
    url(r'',TemplateView.as_view(template_name='404.html')),
]



