from enum import Enum
import enum
import os
from re import M
from django.db import models
from datetime import date, datetime
from django.db.models import Avg
from django.db.models.expressions import F
from rest_framework import exceptions

from Products.models import Collection, Item


class File(models.Model):
    title=models.TextField(null=True,blank=True)
    file=models.FileField(null=True,blank=True,upload_to='attachment/')
    created_at=models.DateField(null=True,blank=True,auto_now=True)
    updated_at=models.DateField(null=True,blank=True)

    def save(self,*args, **kwargs):
        self.updated_at=datetime.now()
        return super().save(*args, **kwargs)

class MediaType(Enum):
    image=1
    video=2

class MediaFile(models.Model):
    title=models.TextField(null=True,blank=True)
    file=models.FileField(null=True,blank=True)
    type=models.IntegerField(choices=((selection.value, selection.name) for selection in MediaType),null=True,blank=True)
    created_at=models.DateField(null=True,blank=True,auto_now=True)
    updated_at=models.DateField(null=True,blank=True)

    def __str__(self):
        return self.title

    def save(self,*args, **kwargs):
        value=self.file.name
        ext = os.path.splitext(value)[1]
        image_ext=['.jpg','.jpeg','.png','.gif','.svg']
        video_ext=['.mp4','.mov','.wmv','.flv','.avi','mkv','.WebM']
        if ext in image_ext:
            self.type=1
        elif ext in video_ext:
            self.type=2
        else:
            raise exceptions.NotAcceptable("Invalid file format.")
        
        self.updated_at=datetime.now()
        return super().save(*args, **kwargs)

class Review(models.Model):
    title= models.TextField(blank=True)
    rate= models.IntegerField(blank=True,null=True)
    description= models.TextField(null=True,blank=True)
    isFeatured=models.BooleanField(default=False)

    user=models.ForeignKey("CustomUser.UserProfile",  verbose_name=("review_user_relation"), on_delete=models.CASCADE)

    
    food=models.ForeignKey('Products.Item',  verbose_name=("review_food_relation"), on_delete=models.CASCADE)

    created_at=models.DateField(null=True,blank=True,auto_now=True)
    updated_at=models.DateField(null=True,blank=True)

    def save(self,*args, **kwargs):
        print("lsjdfhjsdfhljgh;lj")
        avg=Review.objects.filter(food = self.food).exclude(id=self.pk).aggregate(Avg('rate'))
        item_obj=self.food
        print(avg)
        if avg['rate__avg'] is None:
            item_obj.avgRating=self.rate
        else:
            item_obj.avgRating=(avg['rate__avg']+self.rate) / 2
        item_obj.save()
        self.updated_at=datetime.now().date()
        
        return super().save(*args, **kwargs)
    
    def delete(self,  using=None, keep_parents=False):
        avg=Review.objects.filter(food = self.food).aggregate(Avg('rate'))
        item_obj=self.food
        print(avg)
        if avg['rate__avg'] is None:
            item_obj.avgRating=self.rate
        else:
            item_obj.avgRating=avg['rate__avg']
        item_obj.save()
        return super().delete(using, keep_parents)

class adsType(models.Model):
    title= models.TextField(blank=True)
    status=models.BooleanField(default=False)


class Ads(models.Model):
    title= models.TextField(blank=True)
    button= models.TextField(blank=True,null=True)
    image=models.ForeignKey("General.MediaFile",  verbose_name=("ads_image"), on_delete=models.CASCADE,null=True,blank=True)
    food=models.ForeignKey("Products.Item",  verbose_name=("ads_food_relation"), on_delete=models.CASCADE,null=True,blank=True)
    status=models.BooleanField(default=False)
    expiryDate=models.DateTimeField(default=None,blank=True,null=True)
    type=models.ForeignKey(adsType,null=True,blank=True,on_delete=models.CASCADE)

    created_at=models.DateField(null=True,blank=True,auto_now=True)
    updated_at=models.DateField(null=True,blank=True)

    def save(self,*args, **kwargs):
        self.updated_at=datetime.now()
        return super().save(*args, **kwargs)

class Country(models.Model):
    class Meta:
        permissions = (
            ("access_country", "Can access Everything in model"),)
    title=models.TextField()

class State(models.Model):
    class Meta:
        permissions = (
            ("access_state", "Can access Everything in model"),)
    country = models.ForeignKey(Country,on_delete=models.CASCADE)
    title=models.TextField()

class City(models.Model):
    state = models.ForeignKey(State,on_delete=models.CASCADE)
    title=models.TextField()

    def __str__(self):
        return self.title
    


classEnum=((1,'by_weight'),(2,'by_price'))

class ShippingClass(models.Model):
    label=models.TextField(null=True,blank=True)
    type=models.IntegerField(choices=classEnum,default='by_price')
    start=models.FloatField(null=True,blank=True)
    end=models.FloatField(null=True,blank=True)
    price=models.FloatField(null=True,blank=True)
    priority=models.IntegerField(null=True,blank=True)

    def __str__(self):
        return self.label

class ShippingZone(models.Model):
    city=models.ForeignKey(City, on_delete=models.CASCADE)
    shippingClass=models.ManyToManyField(ShippingClass,blank=True)

    status=models.BooleanField(default=False)
    zipcode=models.TextField(null=True,blank=True)
    
    created_at=models.DateField(null=True,blank=True,auto_now=True)
    updated_at=models.DateField(null=True,blank=True)


class AdsChoice(Enum):
    featured=1
    mayLike=2
    offer=3
    seasonal=4
    gallery=5
    reviews=6

class Feed(models.Model):
    type=models.IntegerField(choices=((selection.value, selection.name) for selection in AdsChoice),null=True,blank=True)
    item=models.ForeignKey(Item,on_delete=models.SET_NULL,null=True,blank=True,related_name='home_item')
    items=models.ManyToManyField(Item,blank=True,related_name='home_items')
    images=models.ManyToManyField(MediaFile,null=True,blank=True,related_name='home_images')
    reviews=models.ManyToManyField(Review,blank=True)
    cover_image=models.ForeignKey(MediaFile,on_delete=models.SET_NULL,null=True,blank=True)
    collection=models.ForeignKey(Collection,on_delete=models.SET_NULL,null=True,blank=True,related_name='home_offer')

    created_at=models.DateTimeField(null=True,blank=True,auto_now=True)

    def typeName(self,*args, **kwargs):
        return AdsChoice(self.type).name