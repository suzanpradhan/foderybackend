from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views
urlpatterns = [
    path('', views.UpdateCreate.as_view(),name='product-add'),
    path('<int:id>/', views.UpdateCreate.as_view(),name='product-update'),
    path('all/',views.GetDelete.as_view(),name='product-all'),
    path('all/<int:id>/',views.GetDelete.as_view(),name='product-delete'),
]   