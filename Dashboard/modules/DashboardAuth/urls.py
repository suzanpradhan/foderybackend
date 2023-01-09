from django.contrib import admin
from django.urls import path
from django.urls.conf import include

from Dashboard.modules.DashboardAuth.views import Login
urlpatterns = [
        path('',Login.as_view(), name="admin-login"),
    ]