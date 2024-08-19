"""
URL configuration for django_test project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('import', views.DataManipulation, basename='Load-data')
router.register('delete', views.DataManipulation, basename='Delete-data')


urlpatterns = [
    path('', include(router.urls)),
    path('detail/<str:model_name>/', views.ListModelView.as_view(), name='List-model'),
    path('detail/<str:model_name>/<int:item_id>/', views.DetailModelView.as_view(), name='Detail-model')
]


