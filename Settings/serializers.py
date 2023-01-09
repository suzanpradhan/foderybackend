from django.db import models
from django.db.models import fields
from rest_framework import serializers

from Settings.models import FAQ, AppNotificaiton, AppNotificaitonUser, Coupons, FAQCategory, UnitChoice, appSettings

class GetTermSerializer(serializers.ModelSerializer):
    class Meta:
        model=appSettings
        fields=['terms']

class GetPrivacySerializer(serializers.ModelSerializer):
    class Meta:
        model=appSettings
        fields=['privacy']

class GetAboutSerializer(serializers.ModelSerializer):
    class Meta:
        model=appSettings
        fields=['aboutUs']

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model=FAQ
        fields=["id","question","answer"]

class MultipleFAQSerializer(serializers.ModelSerializer):
    class Meta:
        model=FAQ
        fields=["id","question","answer"]
    
        
class FAQCategorySerializer(serializers.ModelSerializer):
    coverImage = serializers.SerializerMethodField()
    class Meta:
        model=FAQCategory
        fields=['id','coverImage','title']
    
    def get_coverImage(self, obj: FAQCategory):
        return obj.cover_Image.file.url[1:]

class CouponSerializer(serializers.ModelSerializer):
    unitType = serializers.SerializerMethodField()
    def get_unitType(self, obj:Coupons):
        return UnitChoice(obj.unitType).name
    class Meta:
        model=Coupons
        fields=['id','unitType','discount','description']
    
class AppNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model=AppNotificaiton
        fields='__all__'

class AppNotificationUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=AppNotificaitonUser
        fields='__all__'