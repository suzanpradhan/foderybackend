
from types import TracebackType
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import fields
from rest_framework import serializers
from rest_framework.fields import DictField
from Products.models import Item
from QuickOrder.models import PeopleGroupType, Diet, FoodType


class QuickOrderSerializer(serializers.Serializer):
    groupId= serializers.IntegerField(required=True)
    diets=serializers.ListField(required=False, )
    food_types=serializers.ListField(required=False)
    budgetMin=serializers.IntegerField(required=True)
    budgetMax=serializers.IntegerField(required=True)
    hungerLevel=serializers.IntegerField(required=False)

    def validate_diets(self, value):
        if not any((type(i) == dict and i.keys() >= {'people', 'diet'}) for i in value): raise serializers.ValidationError("Diets should contain diet Foreign key and no. of people.")
        return value

    def validate_food_types(self, value):
        if not all((type(i) == int) for i in value): raise serializers.ValidationError("Food Types should contain list of food types Foreign keys.")
        return value

class PeopleGroupTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeopleGroupType
        exclude = ("status",)

class DietSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diet
        exclude = ("status",)

class FoodTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodType
        exclude = ("status",)