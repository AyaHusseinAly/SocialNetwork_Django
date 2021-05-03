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
<<<<<<< HEAD

from django.urls import path ,include
from django.conf import settings
from django.conf.urls.static import static
=======
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
>>>>>>> a9ca0139e276b6d9bad87ed18f0cd3835361793b

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("", include("accounts.urls")),
    path('admin/', admin.site.urls),
    path('posts/', include("posts.urls")),
    path('groups/', include("groups.urls")),
    path('messages/', include("msgnotifications.urls")),



    

]
<<<<<<< HEAD
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
=======


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
>>>>>>> a9ca0139e276b6d9bad87ed18f0cd3835361793b
