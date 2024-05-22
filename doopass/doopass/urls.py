"""
URL configuration for doopass project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from rest_framework import routers

from .views import UserListAPIView, StorageViewSet, BackupViewSet

router = routers.SimpleRouter()
router.register(r"api/storages", StorageViewSet)
router.register(r"api/backups", BackupViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("api/auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
    path("api/users/", UserListAPIView.as_view()),
]

urlpatterns += staticfiles_urlpatterns()
