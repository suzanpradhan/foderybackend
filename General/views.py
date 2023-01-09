
from datetime import date, datetime
import enum
from django.db.models import query
from django.db.models.query_utils import Q
from django.shortcuts import render
from django.utils.decorators import method_decorator
from rest_framework import exceptions, generics, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from CustomUser.models import UserNotificaiton
import random

from General.models import Ads, AdsChoice, Feed, City, Country, MediaFile, Review, State
from General.serilaizers import AdSerializer, CitySerializer, CountrySerializer, MediaFileSerializer, ReviewSerializer, StateSerializer, UserNotificationSerializer
from Products.models import Favorite
from Products.serializers.feed_item_detail_serializer import FeedSerializer
from Products.serilaizers import HomePageItemSerializer
from sweed.decorator import check_token
from django.http.response import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
    JsonResponse,
)
from django.views.generic import TemplateView

class CountryList(generics.ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

class StateList(generics.ListAPIView):
    queryset = State.objects.all()
    serializer_class = StateSerializer

class CityList(generics.ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer

class GetActiveBanner(generics.ListAPIView):
    queryset = Ads.objects.all()
    serializer_class = AdSerializer
    
    def get_queryset(self):
        return self.queryset.filter(status=True,expiryDate__gt=datetime.now())

class GetMediaFile(generics.ListAPIView):
    queryset = MediaFile.objects.all()
    serializer_class = MediaFileSerializer

    def get_queryset(self):
        return self.queryset.filter(id=self.kwargs['id'])
    
@method_decorator(check_token, name='dispatch')
class CreateReview(generics.CreateAPIView):
    serializer_class = ReviewSerializer

    def post(self,request,*args, **kwargs):
        request.data['user']=self.kwargs['user'].id
        return self.create(request,*args, **kwargs)


@method_decorator(check_token, name='dispatch')
class GetUpdateDestroyReview(generics.RetrieveUpdateDestroyAPIView):
    queryset=Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_field='id'

    def get(self,request,*args, **kwargs):
        try:
            if Review.objects.filter(food_id=self.kwargs['id'],user=self.kwargs['user']).exists():
                return Response(self.serializer_class(Review.objects.get(food_id=self.kwargs['id'],user=self.kwargs['user'])).data)
            else:
                return HttpResponseBadRequest("Review doesnot exist.")
        except:
            return HttpResponseBadRequest(None)
    def post(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        review_obj=Review.objects.filter(id=kwargs['id'],user=self.kwargs['user']).first()
        print(review_obj)

        if review_obj is None:
            raise exceptions.NotFound("Review not found.")
        review_obj.delete()
        return Response("Review deleted successfully.")

@method_decorator(check_token, name='dispatch')
class GetReviewByFood(generics.ListAPIView):
    queryset=Review.objects.all()
    serializer_class = ReviewSerializer

    # def get(self, request, *args, **kwargs):
    #     id=self.kwargs['id']
    #     query=self.queryset.filter(~Q(user=self.kwargs['user']),food_id=id)
    #     serializer = self.get_serializer(query, many=True)
    #     page = self.paginate_queryset(query)
    #     data={
    #         "count":self.queryset.filter(food_id=id).count(),
    #         "data":serializer.data
    #     }
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(data)
    #     response=Response()
        
        
    #     response.data=data
    #     return response


    def get_queryset(self):
        id=self.kwargs['id']
        sortBy = ["time", 'rating']
        queryData = self.queryset.filter(~Q(user=self.kwargs['user']),food_id=id)
        
        orderBy = self.request.query_params.get("order_by")
        if orderBy is not None:
            print(orderBy)
            if orderBy in sortBy:
                if orderBy == sortBy[0]:
                    queryData = queryData.order_by("-created_at")
                elif orderBy == sortBy[1]:
                    queryData = queryData.order_by("-rate")
        # response=Response()
        return queryData
    # def get(self,request,*args, **kwargs):
    #     id=self.kwargs['id']
    #     queryset=Review.objects.all()

    #     response=Response()
    #     query=queryset.filter(~Q(user=self.kwargs['user']),food_id=id)
    #     print(query.count())
    #     response.data={
    #         "count":query.count(),
    #         "results":ReviewSerializer(query,many=True).data
    #     }
    #     return response
    
@method_decorator(check_token, name='dispatch')
class GetNotiByUser(generics.ListAPIView):
    queryset            = UserNotificaiton.objects.all()
    serializer_class    = UserNotificationSerializer

    def get_queryset(self):
        user=self.kwargs['user'].id
        return self.queryset.filter(user_id=user)


@method_decorator(check_token, name='dispatch')
class SeeNotificaiton(APIView):
    def get(self,request,id):
        model_obj=UserNotificaiton.objects.filter(id=id).first()
        if model_obj is None:
            raise exceptions.NotFound("Notification doesn't exist.")
        model_obj.seen=True
        model_obj.save()

        return Response({"status:success"})

@method_decorator(check_token, name='dispatch')
class UnseeNotificaiton(APIView):
    def get(self,request,id):
        model_obj=UserNotificaiton.objects.filter(id=id).first()
        if model_obj is None:
            raise exceptions.NotFound("Notification doesn't exist.")
        model_obj.seen=False
        model_obj.save()

        return Response({"status:success"})

@method_decorator(check_token, name='dispatch')
class GetUnseenNotificaiton(generics.ListAPIView):
    queryset            = UserNotificaiton.objects.all()
    serializer_class    = UserNotificationSerializer

    def get_queryset(self):
        user=self.kwargs['user'].id
        return self.queryset.filter(user_id=user,seen=False)


@method_decorator(check_token, name='dispatch')
class GetSeenNotificaiton(generics.ListAPIView):
    queryset            = UserNotificaiton.objects.all()
    serializer_class    = UserNotificationSerializer

    def get_queryset(self):
        user=self.kwargs['user'].id
        return self.queryset.filter(user_id=user,seen=True)

@method_decorator(check_token, name='dispatch')
class DeleteUserNoti(generics.DestroyAPIView):

    queryset            = UserNotificaiton.objects.all()
    serializer_class    = UserNotificationSerializer

@method_decorator(check_token, name='dispatch')
class GetFeed(APIView):
    def get(self,request,*args, **kwargs):
        queryset=Feed.objects.filter().order_by('-created_at')
        setter={"featured":['coverImage','item'],
        "mayLike":['items'],
        "offer":['coverImage','item'],
        "seasonal":['collection'],
        "gallery":['gallery','item'],
        "reviews":['item','reviews']}
        favourite=Favorite.objects.filter(user=self.kwargs['user'],isLiked=True)
        items=[]
        for _ in favourite:
            items.append(_.product)
        items=list(set(items))
        # favourite_data={"type":"favorite","data":FeedItemDetailSerializer(items,many=True).data}
        data=[]
        for _ in queryset:
            serializer=FeedSerializer(_,many=False,customizeFields=setter.get(AdsChoice(_.type).name))
            data.append({"type":AdsChoice(_.type).name,
                            "data":serializer.data})
        
        # if len(data)>=4:
        #     data.insert(3,favourite_data)
        # else:
        #     data.append(favourite_data)

        return Response(data)

class GetFeedBeta(generics.ListAPIView):
    queryset = Feed.objects.all()
    serializer_class = FeedSerializer

    def get_queryset(self):
        return self.queryset.order_by('-created_at')

class TermsAndConditions(TemplateView):
    template_name = "terms_and_conditions.html"

class PrivacyPolicy(TemplateView):
    template_name = "privacy_policy.html"