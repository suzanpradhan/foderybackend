import binascii
import os
import secrets
from statistics import mode
from tarfile import TarError
from django.db import models
from django.contrib.auth import validators
from django.contrib.auth.models import AbstractUser, User
from datetime import datetime
from django.utils import tree
from enum import Enum

from rest_framework import serializers
from General.models import City, Country, MediaFile, State
from . import manager as user_manager
from django.conf import settings
from django.core.files import File
from urllib.request import urlopen
from tempfile import NamedTemporaryFile
import random,string
def random_key(length):
	key = ''
	for i in range(length):
		key += random.choice(string.hexdigits)
	return key

class Gender(Enum):
    male=1
    female=2
    nonBinary=3

class Profile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='user', on_delete=models.CASCADE, null=True)
    fname = models.CharField(max_length=24, null=True)
    lname = models.CharField(max_length=24, null=True)
    phone = models.TextField(null=True,blank=True)
    avatar = models.ImageField(upload_to='avatar/',null=True, blank=True)
    coverImage = models.ImageField(upload_to='coverImage/',null=True, blank=True)
    bio=models.TextField(null=True,blank=True)
    gender=models.IntegerField(choices=((selection.value, selection.name) for selection in Gender),default=1)
    isStaff=models.BooleanField(default=False)
    image_url = models.URLField(null=True,blank=True)
    isPhoneVerified = models.BooleanField(default=False)
    requestTimes = models.IntegerField(default=0, null=True, blank=True)
    lastRequestTimes = models.IntegerField(default=0, null=True, blank=True)
    update_at_rt = models.DateTimeField(null=True, blank=True)
    refer_code=models.TextField(null=True)
    publicIp = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.refer_code == None:
            tempCode = random_key(6)
            while True:
                if Profile.objects.filter(refer_code=tempCode).exists():
                    tempCode = random_key(6)
                else:
                    break
            self.refer_code=tempCode

        if self.image_url and not self.avatar:
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urlopen(self.image_url).read())
            img_temp.flush()
            self.avatar.save(f"image_{self.pk}.png", File(img_temp))
        super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.email

class UserProfile(AbstractUser):
    email = models.EmailField(('email address'), unique=True)
    is_active=models.BooleanField(default=False)
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ['email']
    objects = user_manager.UserProfileManager()

    def __str__(self):
        return self.username

    def profile_exists(self):
        return Profile.objects.filter(user_id = self.pk).exists()
    
    def profile(self) -> Profile:
        if self.profile_exists():
            return Profile.objects.get(user_id = self.pk) or None

    def profile_full_name(self) -> str:
        if self.profile_exists():
            
            if self.profile().fname:
                fname=self.profile().fname
            else:
                fname=""
            if self.profile().lname:
                lname=self.profile().lname
            else:
                lname=""
            return fname + " " + lname

# class SoicalID(models.Model):
#     facebook=models.TextField(null=True,blank=True)
#     google=models.TextField(null=True,blank=True)

#     user=models.ForeignKey(UserProfile,on_delete=models.CASCADE)

class Address(models.Model):
    user= models.ForeignKey(UserProfile, on_delete=models.CASCADE,null=True)
    label=models.TextField(null=True,blank=True)
    companyName=models.TextField(null=True,blank=True)
    isDefault=models.BooleanField(default=False)

    fname =models.TextField(null=True,blank=True)
    lname =models.TextField(null=True,blank=True)
    phone =models.TextField(null=True,blank=True)
    streetAdd1 =models.TextField(null=True,blank=True)
    streetAdd2 =models.TextField(null=True,blank=True)
    zipCode =models.TextField(null=True,blank=True)

    state=models.ForeignKey(State,  verbose_name=("deliver_address_state_realtion"), on_delete=models.CASCADE)
    country=models.ForeignKey(Country,  verbose_name=("deliver_address_country_realtion"), on_delete=models.CASCADE)
    city=models.ForeignKey(City,  verbose_name=("deliver_address_city_realtion"), on_delete=models.CASCADE)
    
    latitude=models.FloatField(null=True,blank=True)
    longitude=models.FloatField(null=True,blank=True)

class Refer(models.Model):
    referedBy=models.ForeignKey(UserProfile,on_delete=models.SET_NULL,related_name='referBy',null=True)
    referedTo=models.ForeignKey(UserProfile,on_delete=models.SET_NULL,null=True)
    status=models.BooleanField(default=False)

class UserNotificaiton(models.Model):
    title=models.TextField(null=True,blank=True)
    description=models.TextField(null=True,blank=True)
    action=models.TextField(null=True,blank=True)
    date=models.DateField(auto_now=True,null=True)
    seen=models.BooleanField(default=False)
    user=models.ForeignKey(UserProfile,on_delete=models.CASCADE,null=True,blank=True)