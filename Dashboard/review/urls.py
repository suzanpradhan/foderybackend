from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views
urlpatterns = [
    path('all/<int:id>', views.Get.as_view(),name='review-all'),
    path('food/', views.ReviewTemplate.as_view(),name='review-food'),
    path('<int:id>/', views.Delete.as_view(),name='review-delete'),
    path('update/<int:id>/', views.Update.as_view(),name='review-update'),
]   