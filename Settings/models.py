from enum import Enum
from os import truncate
from django.contrib.auth.models import User
from django.db import models
from datetime import datetime
from django.db.models.deletion import CASCADE

from django.db.models.fields import BooleanField

from CustomUser.models import UserProfile
from General.models import MediaFile


class Paymentcredentials(models.Model):
    title= models.TextField(blank=True)
    publicKey=models.TextField(blank=True,null=True)

class SocialAuth(models.Model):
    title= models.TextField(blank=True)
    status=models.BooleanField(default=False)
    appID=models.TextField(blank=True,null=True)
    appSecret=models.TextField(blank=True,null=True)

class FAQCategory(models.Model):
    title= models.TextField(blank=True)
    
    cover_Image=models.ForeignKey(MediaFile,on_delete=CASCADE,null=True,blank=True)

    createdAt=models.DateField(auto_now=True)
    updatedAt=models.DateField(null=True,blank=True)

    def save(self, *args, **kwargs):

        self.updated_at=datetime.now()
        return super().save(*args, **kwargs)


class FAQ(models.Model):
    question=models.TextField(blank=True,null=True)
    answer=models.TextField(blank=True,null=True)

    faqCategory=models.ForeignKey(FAQCategory, on_delete=models.CASCADE,null=True,blank=True)
    
    createdAt=models.DateField(auto_now=True)
    updatedAt=models.DateField(null=True,blank=True)

    def save(self, *args, **kwargs):

        self.updated_at=datetime.now()
        return super().save(*args, **kwargs)

currencyPos=((1,'prefix'),(2,'suffix'))

class Currency(models.Model):
    title= models.TextField(blank=True)
    symbol= models.CharField(null=True,blank=True,max_length=1)
    place=models.IntegerField(choices=currencyPos,default=1)
    isDefault=models.BooleanField(default=False)
    status=models.BooleanField(default=False)
    transferRate=models.IntegerField(blank=True,null=True)

class Tax(models.Model):
    value=models.IntegerField(null=True,blank=True)
    isDefault=models.BooleanField(default=False)

class appSettings(models.Model):
    appName=models.TextField(null=True,blank=True)
    shortDescription=models.TextField(null=True,blank=True)
    image=models.ForeignKey("General.MediaFile",  verbose_name=("app_icon"), on_delete=models.CASCADE,null=True,blank=True)
    isDarkMode=models.BooleanField(default=False)
    terms=models.TextField(null=True,blank=True) 
    privacy=models.TextField(null=True,blank=True) 
    aboutUs=models.TextField(null=True,blank=True)
    versionNumber=models.TextField(null=True,blank=True)
    referReward=models.IntegerField(null=True,blank=True)
    currency=models.ForeignKey(Currency,null=True,blank=True, on_delete=models.CASCADE)
    facebook=models.TextField(null=True,blank=True)
    instagram=models.TextField(null=True,blank=True)
    github=models.TextField(null=True,blank=True)
    cashBackPercentage = models.IntegerField(default=0, null=True, blank=True)
    supportPhone = models.TextField(null=True, blank=True)
    supportEmail = models.CharField(null=True, blank=True, max_length=255)
    supportAddress = models.TextField(null=True, blank=True)
    companyName = models.TextField(null=True, blank=True)


UnitChoices=((1,'Km'),(2,'m'),(3,'mi'))

class GoogleMapSetting(models.Model):
    googleMapKey=models.TextField(null=True,blank=True)
    distanceUnit=models.IntegerField(choices=UnitChoices,default=1)

class SMTP(models.Model):
    mailHost=models.TextField(null=True,blank=True)
    mailPort=models.TextField(null=True,blank=True)
    encryption=models.TextField(null=True,blank=True)
    username=models.TextField(null=True,blank=True)
    password=models.TextField(null=True,blank=True)

class PushNotification(models.Model):
    firebaseCloudKey=models.TextField(null=True,blank=True)
    apiKey=models.TextField(null=True,blank=True)
    databaseUrl=models.TextField(null=True,blank=True)
    storageBucket=models.TextField(null=True,blank=True)
    appId=models.TextField(null=True,blank=True)
    authDomain=models.TextField(null=True,blank=True)
    projectID=models.TextField(null=True,blank=True)
    senderID=models.TextField(null=True,blank=True)
    measurementID=models.TextField(null=True,blank=True)

unitChoice=((1,'%'),(2,'number'))
class UnitChoice(Enum):
    percent=1
    amount=2
class Coupons(models.Model):
    code=models.TextField(null=True,blank=True)
    unitType=models.IntegerField(choices=((units.value,units.name) for units in UnitChoice),default=1)
    discount=models.IntegerField(null=True,blank=True)
    description=models.TextField(null=True,blank=True)
    expiresAt=models.DateTimeField(null=True,blank=True)
    status=models.BooleanField(default=False)
    isReward=models.BooleanField(default=False)
    
    createdAt=models.DateField(auto_now=True)
    updatedAt=models.DateField(null=True,blank=True)

    def save(self, *args, **kwargs):

        self.updated_at=datetime.now()
        return super().save(*args, **kwargs)

class User_Coupons(models.Model):
    user=models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    coupon=models.ForeignKey(Coupons, on_delete=models.CASCADE)
    used=models.BooleanField(default=False)

class AppNotificaiton(models.Model):
    title=models.TextField(null=True,blank=True)
    description=models.TextField(null=True,blank=True)

    icon=models.ForeignKey(MediaFile,on_delete=models.CASCADE, related_name='appNoti_image',null=True,blank=True)
    image=models.ForeignKey(MediaFile,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.title

class AppNotificaitonUser(models.Model):
    appNotification=models.ForeignKey(AppNotificaiton,on_delete=models.CASCADE,null=True,blank=True)
    user=models.ForeignKey(UserProfile,on_delete=models.CASCADE,null=True,blank=True)
    seen=models.BooleanField(default=False)

class Reward(models.Model):
    points=models.IntegerField(default=0)
    user=models.ForeignKey(UserProfile,blank=True,on_delete=models.CASCADE)

class RewardType(Enum):
    percent=1
    amount=2

class RewardCollection(models.Model):
    discount=models.IntegerField(default=0)
    type = models.IntegerField(choices=((rewardType.value,rewardType.name) for rewardType in RewardType),default=2)
    cost=models.IntegerField()

class RewardCoupon(models.Model):
    coupons=models.ForeignKey(Coupons,on_delete=models.SET_NULL,null=True,blank=True,related_name='reward_coupon')
    user=models.ForeignKey(UserProfile,on_delete=models.CASCADE,null=True,blank=True,related_name='reward_user')

class MaintainanceMode(models.Model):
    status=models.BooleanField(default=True)
    message=models.TextField(null=True,blank=True,default="MaintainanceMode")

class OrderInfo(models.Model):
    billNo=models.IntegerField(default=0)
    receiptNo=models.IntegerField(default=0)