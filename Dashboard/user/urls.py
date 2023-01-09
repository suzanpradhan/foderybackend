from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views
urlpatterns = [
    path('user/<int:id>/', views.UpdateCreate.as_view(),name='user-update'),
    path('user/', views.UpdateCreate.as_view(),name='user-add'),
    path('user/all/', views.GetDelete.as_view(),name='user-all'),
    path('user/all/<int:id>/', views.GetDelete.as_view(),name='user-delete'),
    
]   