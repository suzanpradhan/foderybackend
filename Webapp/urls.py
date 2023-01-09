from django.urls import path
from django.urls.conf import include
from .views import * 
urlpatterns = [
    path('', LandingPage.as_view(), name="landing-name"),
]