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
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from rest_framework import routers

from .views import UserView, StorageView

router = routers.DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),

    path('api/users/', UserView.as_view(http_method_names=['get'])),
    path('api/users/<int:id>/', UserView.as_view(http_method_names=['get'])),
    path('api/users/create/', UserView.as_view(http_method_names=['post'])),
    path('api/users/update/', UserView.as_view(http_method_names=['put'])),
    path('api/users/delete/', UserView.as_view(http_method_names=['delete'])),

    path('api/storages/', StorageView.as_view(http_method_names=['get'])),
    path('api/storages/<int:id>/', StorageView.as_view(http_method_names=['get'])),
    path('api/storages/of-owner/<int:owner_id>/', StorageView.as_view(http_method_names=['get'])),
    path('api/storages/create/', StorageView.as_view(http_method_names=['post'])),
    path('api/storages/update/', StorageView.as_view(http_method_names=['put'])),
    path('api/storages/delete/', StorageView.as_view(http_method_names=['delete']))
]

urlpatterns += staticfiles_urlpatterns()
