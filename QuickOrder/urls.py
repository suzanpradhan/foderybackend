from django.contrib import admin
from django.urls import path
from django.urls.conf import include

from .views import QuickOrder, GetPeopleGroupType, GetAllDiets, GetAllFoodTypes
urlpatterns = [
    path('items', QuickOrder.as_view()),
    path('allPeopleGroupType', GetPeopleGroupType.as_view()),
    path('allDiets', GetAllDiets.as_view()),
    path('allFoodTypes', GetAllFoodTypes.as_view()),
]
