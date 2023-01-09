from django.contrib import admin
from django.urls import path
from django.urls.conf import include

from General.views import *

urlpatterns = [
    path('country/', CountryList.as_view()),
    path('state/', StateList.as_view()),
    path('city/', CityList.as_view()),
    path('get_active_ads/', GetActiveBanner.as_view()),
    path('get_media_file/<int:id>/', GetMediaFile.as_view()),
    path('addReview/', CreateReview.as_view()),
    path('getUpdateDeleteReview/<int:id>/', GetUpdateDestroyReview.as_view()),
    path('get_review_food/<int:id>/', GetReviewByFood.as_view()),
    path('getUnseenNotification/<int:id>/',GetUnseenNotificaiton.as_view()),
    path('getSeenNotification/<int:id>/',GetSeenNotificaiton.as_view()),
    path('seeNotification/<int:id>/',SeeNotificaiton.as_view()),
    path('unSeeNotification/<int:id>/',UnseeNotificaiton.as_view()),
    path('getUserNotification/<int:id>/',GetNotiByUser.as_view()),
    path('homescreen/',GetFeed.as_view()),
    path('get_feed', GetFeedBeta.as_view()),
    path('terms_and_conditions', TermsAndConditions.as_view()),
    path('privacy_policy', PrivacyPolicy.as_view())
]
