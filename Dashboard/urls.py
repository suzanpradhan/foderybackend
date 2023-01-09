from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from .views import * 
urlpatterns = [
    path('', include('Dashboard.user.urls')),
    path('', include('Dashboard.roles.urls')),
    path('', include('Dashboard.order.urls')),
    path('review/', include('Dashboard.review.urls')),
    path('products/', include('Dashboard.products.urls')),
    path('collection/', include('Dashboard.collection.urls')),
    path('settings/', include('Dashboard.settings.urls')),
    path('logout/',Logout.as_view(),name='logout'),
    path('home/',HomePage.as_view(),name='home')
    ]