from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views
urlpatterns = [
    path('role/<int:id>/', views.UpdateCreate.as_view(),name='role-update'),
    path('role/', views.UpdateCreate.as_view(),name='role-add'),
    path('role/all/',views.GetDelete.as_view(),name='role-all'),
    path('role/perms/',views.Get.as_view(),name='role-perms'),
    path('role/all/<int:id>/',views.GetDelete.as_view(),name='role-delete'),
]   