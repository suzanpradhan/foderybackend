from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from rest_framework import views
from rest_framework.permissions import IsAuthenticated

from .views import BasicInfo, CheckMaintainance, ExchangeReward, GetAbout, GetAppNotificaion, GetCouponByCode, GetFAQbyCategory, GetSeenNotificaiton,GetTerm,GetPrivacy,GetFAQCategory,GetFAQ, GetUnseenNotificaiton, SeeNotificaiton, UnseeNotificaiton
urlpatterns = [
    path('getTerm/',GetTerm.as_view()),
    path('getPrivacy/',GetPrivacy.as_view()),
    path('getAbout/',GetAbout.as_view()),
    path('getAppInfo/',BasicInfo.as_view()),
    path('getFAQ/<int:id>/',GetFAQ.as_view()),
    path('getFAQCategory/',GetFAQCategory.as_view()),
    path('getFAQCategory/<int:id>/',GetFAQbyCategory.as_view()),
    path('getCouponByCode/',GetCouponByCode.as_view()),
    path('getAllAppNotification/',GetAppNotificaion.as_view()),
    path('getUnseenNotification/<int:id>/',GetUnseenNotificaiton.as_view()),
    path('getSeenNotification/<int:id>/',GetSeenNotificaiton.as_view()),
    path('seeNotification/<int:id>/',SeeNotificaiton.as_view()),
    path('unSeeNotification/<int:id>/',UnseeNotificaiton.as_view()),
    path('exchange_reward_points/',ExchangeReward.as_view()),
    path('check_maintainance/',CheckMaintainance.as_view()),

]
