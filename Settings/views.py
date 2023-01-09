import hashlib
from re import A, M, T
from django import http
from django.db import models
from django.http.response import HttpResponse, HttpResponseForbidden
from django.shortcuts import render
from django.utils.decorators import method_decorator
from rest_framework import exceptions, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime
from django.utils import timezone as time

from CustomUser.models import UserProfile
from sweed.decorator import check_token
from .models import FAQ, AppNotificaiton, AppNotificaitonUser, Coupons, FAQCategory, MaintainanceMode, Reward, RewardCollection, RewardCoupon, User_Coupons, appSettings
from .serializers import AppNotificationSerializer, AppNotificationUserSerializer, CouponSerializer, FAQCategorySerializer, FAQSerializer, GetAboutSerializer, GetPrivacySerializer, GetTermSerializer, MultipleFAQSerializer
from django.views.generic import TemplateView
class GetTerm(TemplateView):
    template_name = "terms.html"

    def get(self,request):
        return render(request,template_name=self.template_name)
class GetPrivacy(TemplateView):
    template_name = "privacy.html"

    def get(self,request):
        return render(request,template_name=self.template_name)


class GetAbout(generics.ListAPIView):
    queryset            = appSettings.objects.all()
    serializer_class    = GetAboutSerializer

    def get_queryset(self):
        return self.queryset.filter(id=1)

class GetFAQ(generics.RetrieveAPIView):
    
    queryset            = FAQ.objects.all()
    serializer_class    = FAQSerializer
    lookup_field        ='id'
    

class GetFAQCategory(generics.ListAPIView):
    queryset            = FAQCategory.objects.all()
    serializer_class    = FAQCategorySerializer
    
class GetFAQbyCategory(APIView):

    def get(self,request,*args, **kwargs):
        id=kwargs["id"]
        query=FAQ.objects.filter(faqCategory_id=id)
        serializer=MultipleFAQSerializer(query,many=True)

        return Response(serializer.data)

@method_decorator(check_token, name='dispatch')
class GetCouponByCode(APIView):
    queryset            = Coupons.objects.all()
    serializer_class    = CouponSerializer

    def post(self,request,*args, **kwargs):
        user=self.kwargs['user'].id
        code=request.data['code']
        code_query=self.queryset.filter(code=code)
        if len(code_query)>=1:
            coupon_obj=Coupons.objects.filter(code=code).first()
            if coupon_obj is None:
                raise exceptions.NotFound("Coupon not found.")

            date_query=code_query.filter(expiresAt__gt=time.now())
            user_obj=UserProfile.objects.filter(id=user).first()
            if user_obj is None:
                raise exceptions.NotFound("User not found.")
            if len(date_query)>=1 and coupon_obj.status is True:

                return Response(CouponSerializer(date_query[0]).data)
                
            else:
                return Response({"status":"error","message":"The coupon code is expired."},status=409)
            
        else:
            return HttpResponse({"status":"error","message":"The coupon code is invalid."},status=409)


class GetAppNotificaion(generics.ListAPIView):
    queryset            = AppNotificaiton.objects.all()
    serializer_class    = AppNotificationSerializer

@method_decorator(check_token, name='dispatch')
class GetUnseenNotificaiton(generics.ListAPIView):
    queryset            = AppNotificaitonUser.objects.all()
    serializer_class    = AppNotificationUserSerializer

    def get_queryset(self):
        user=self.kwargs['user'].id
        return self.queryset.filter(user_id=user,seen=False)

@method_decorator(check_token, name='dispatch')
class GetSeenNotificaiton(generics.ListAPIView):
    queryset            = AppNotificaitonUser.objects.all()
    serializer_class    = AppNotificationUserSerializer

    def get_queryset(self):
        user=self.kwargs['user'].id
        return self.queryset.filter(user_id=user,seen=True)

@method_decorator(check_token, name='dispatch')
class SeeNotificaiton(APIView):
    def get(self,request,id):
        model_obj=AppNotificaitonUser.objects.filter(id=id).first()
        if model_obj is None:
            raise exceptions.NotFound("Notification not found.")
        model_obj.seen=True
        model_obj.save()

        return Response({"status:success"})

@method_decorator(check_token, name='dispatch')
class UnseeNotificaiton(APIView):
    def get(self,request,id):
        model_obj=AppNotificaitonUser.objects.filter(id=id).first()
        if model_obj is None:
            raise exceptions.NotFound("Notification not found.")
        model_obj.seen=False
        model_obj.save()

        return Response({"status:success"})

@method_decorator(check_token, name='dispatch')
class ExchangeReward(APIView):
    def post(self,request,*args, **kwargs):
        rewardCollection=request.data.get('reward')
        user=self.kwargs['user'].id
        reward_query=RewardCollection.objects.filter(id=rewardCollection)
        user_reward_query=Reward.objects.filter(user_id=user)
        reward_obj=reward_query[0]
        user_reward=user_reward_query[0]       
        if reward_query.exists():
            if user_reward_query.exists() and user_reward.points>=reward_obj.cost:
                coupon_obj=Coupons.objects.create(code=hashlib.sha3_256(str(user).encode()).hexdigest(),unitType=reward_obj.type,discount=reward_obj.discount,description='Reward',status=True,isReward=True,expiresAt=time.now()+time.timedelta(days=36450))
                user_reward.points=user_reward.points-reward_obj.cost
                user_reward.save()
                RewardCoupon.objects.create(coupons=coupon_obj,user_id=user)
                
                return HttpResponse(coupon_obj.code)
            else:
                raise HttpResponseForbidden("You don't have enough points.")
        else:
                raise HttpResponseForbidden("The offer doesn't exits.")

class CheckMaintainance(APIView):
    def get(self,request,*args, **kwargs):

        model_obj,created=MaintainanceMode.objects.get_or_create(id=1)
        response=Response()
        response.data={
            "status":model_obj.status,
            "message":model_obj.message
        }
        return response

class BasicInfo(APIView):
    def get(self,request):
        obj,created=appSettings.objects.get_or_create(id=1)
        response=Response()

        
        response.data={
            "aboutUs":obj.aboutUs,
            "versionNumber":obj.versionNumber,
            "terms":obj.terms,
            "privacy":obj.privacy,
            "facebook":obj.facebook,
            "instagram":obj.instagram,
            "github":obj.github,
            "support_phone": obj.supportPhone,
            "support_email": obj.supportEmail,
            "support_address": obj.supportAddress,
            "company_name": obj.companyName
        }
        
        return response