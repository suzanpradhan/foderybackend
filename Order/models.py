import binascii
import os
from pyexpat import model
import secrets
from django.contrib.auth.models import User
from django.db import models
from datetime import datetime
import bcrypt
from django.utils import tree
from CustomUser.models import UserProfile
from General.models import City, Country, State
from Products.models import Extra, Variant
import hashlib
from enum import Enum
from Settings.models import Coupons, Currency, OrderInfo, Tax

import random
import string

def random_key(length):
	key = ''
	for i in range(length):
		key += random.choice(string.hexdigits)
	return key

class CartItem(models.Model):
    quantity=models.IntegerField(null=True,blank=True)
    items=models.ForeignKey("Products.Item",  verbose_name=("cart_items_relation"),on_delete=models.CASCADE,null=True,blank=True)
    variant=models.ForeignKey(Variant, on_delete=models.CASCADE,blank=True,null=True)
    extra=models.ManyToManyField(Extra,blank=True)


class Cart(models.Model):
    identifier=models.CharField(unique=True,null=True,blank=True,max_length=64)
    
    user=models.ForeignKey(UserProfile,on_delete=models.CASCADE,null=True,blank=True,unique=True)

    items=models.ManyToManyField(CartItem)
    
    createdAt=models.DateField(auto_now=True)
    updatedAt=models.DateField(null=True,blank=True)

    def save(self, *args, **kwargs):
        if self.identifier == None:
            tempIdentifier = secrets.token_hex(6)
            while True:
                if Cart.objects.filter(identifier=tempIdentifier).exists():
                    tempIdentifier = secrets.token_hex(6)
                else:
                    break
            self.identifier=tempIdentifier
        self.updated_at=datetime.now()
        return super().save(*args, **kwargs)

class DeliverAddress(models.Model):
    fname =models.TextField(null=True,blank=True)
    lanme =models.TextField(null=True,blank=True)
    phone =models.TextField(null=True,blank=True)
    streetAdd1 =models.TextField(null=True,blank=True)
    streetAdd2 =models.TextField(null=True,blank=True)
    zipCode =models.TextField(null=True,blank=True)

    state=models.ForeignKey(State,  verbose_name=("deliver_address_state_realtion"), on_delete=models.CASCADE)
    country=models.ForeignKey(Country,  verbose_name=("deliver_address_country_realtion"), on_delete=models.CASCADE)
    city=models.ForeignKey(City,  verbose_name=("deliver_address_city_realtion"), on_delete=models.CASCADE)
    
    
    latitude=models.FloatField(null=True,blank=True)
    longitude=models.FloatField(null=True,blank=True)

unitChoice=((1,'%'),(2,'number'))

class Discount(models.Model):
    unitType=models.IntegerField(choices=unitChoice,default=1)
    amount=models.IntegerField(null=True,blank=True)
    description=models.TextField(null=True,blank=True)

class OrderItem(models.Model):

    quantity=models.IntegerField(null=True,blank=True)
    item=models.ForeignKey("Products.Item",  verbose_name=("order_items_relation"),on_delete=models.CASCADE,null=True,blank=True)
    variant=models.ForeignKey(Variant, on_delete=models.CASCADE,blank=True,null=True)
    extras=models.ManyToManyField(Extra,blank=True)
    item_price = models.FloatField(default=0,null=True, blank=True)
    extras_price = models.FloatField(default=0,null=True, blank=True)
    total_price = models.FloatField(default=0,null=True, blank=True)

    def get_variant_name(self):
        tempName = ""
        if (self.variant):
            for i, element in enumerate(self.variant.items.all()):
                if (i == (self.variant.items.count() - 1)):
                    tempName = tempName + element.attributeItem.title
                else:
                    tempName = tempName + element.attributeItem.title + " /"
        return tempName

class Transaction(models.Model):
    user=models.ForeignKey("CustomUser.UserProfile",  verbose_name=("transaction_user_relation"), on_delete=models.CASCADE)
    
    token=models.TextField(null=True,blank=True)
    mobile=models.TextField(null=True,blank=True)

# statusEnum=((1,'pending'),(2,'Preparing'),(3,'delivering'),(4,'delivered'))

class OrderStatus(Enum):
    pending = 1
    Preparing = 2
    delivering = 3
    delivered = 4

class ExtraOrder(models.Model):
    quantity=models.IntegerField(null=True,blank=True)
    extra=models.ForeignKey(Extra,blank=True,on_delete=models.SET_NULL,null=True)


class Order(models.Model):
    description= models.TextField(null=True,blank=True)
    billNo=models.IntegerField(default=0)
    receiptNo=models.IntegerField(default=0)
    note= models.TextField(null=True,blank=True)
    status=models.IntegerField(choices=((status.value, status.name) for status in OrderStatus),default=1)
    isActive=models.BooleanField(default=False)
    identifier=models.TextField(null=True,blank=True)
    order_number=models.TextField(null=True,blank=True)
    amount=models.FloatField(null=True,blank=True)
    taxAmount=models.FloatField(null=True,blank=True)
    shipAmount=models.FloatField(null=True,blank=True)
    extraAmount=models.FloatField(null=True,blank=True)
    couponAmount=models.FloatField(null=True,blank=True)
    discountAmount=models.FloatField(null=True,blank=True)
    grandAmount=models.FloatField(null=True,blank=True)
    cashBackReward = models.IntegerField(null=True, blank=True)
    totalWeight=models.FloatField(null=True,blank=True)
    isPaid = models.BooleanField(default=False, null=True, blank=True)
    isTransactionConfirmed = models.BooleanField(default=False, null=True, blank=True)
    transaction=models.ForeignKey(Transaction,  verbose_name=("order_transaction_realtion"), on_delete=models.CASCADE,null=True,blank=True)
    DeliveryAddress=models.ForeignKey(DeliverAddress,  verbose_name=("order_delivery_address_realtion"), on_delete=models.CASCADE,null=True,blank=True)
    deliveryPerson=models.ForeignKey(UserProfile,related_name="order_delivery_person_realtion",on_delete=models.CASCADE,null=True,blank=True)
    coupon=models.ForeignKey(Coupons,on_delete=models.CASCADE,null=True,blank=True)
    extras=models.ManyToManyField(ExtraOrder,blank=True)
    discount=models.ForeignKey(Discount,on_delete=models.SET_NULL,null=True,blank=True)
    currency=models.ForeignKey(Currency,on_delete=models.SET_NULL,null=True,blank=True)
    tax=models.ForeignKey(Tax,on_delete=models.SET_NULL,null=True,blank=True)
    user=models.ForeignKey("CustomUser.UserProfile",  verbose_name=("order_user_relation"), on_delete=models.CASCADE)
    items=models.ManyToManyField(OrderItem,  verbose_name=("order_items_relation"),blank=True)
    createdAt=models.DateTimeField(null=True,blank=True,auto_now=True)
    deliveredAt = models.DateTimeField(null=True, blank=True)
    updatedAt=models.DateField(null=True,blank=True)
    
    def save(self, *args, **kwargs):
        if self.identifier == None or self.identifier == "":
            self.identifier=bcrypt.hashpw(str(str(self.id)).encode(), bcrypt.gensalt())
            generated_key=random_key(8)
            flag=False

            while not flag:
                if Order.objects.filter(order_number=generated_key).exists():
                    generated_key=random_key(8)
                else:
                    self.order_number=generated_key
                    flag=True
        self.updated_at=datetime.now()
        return super().save(*args, **kwargs)
    
