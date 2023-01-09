from os import set_inheritable
from django.contrib.auth.models import Group, User
from django.db.models import fields, manager
from rest_framework import serializers
from .models import Address, Profile,UserProfile
from CustomUser import models

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username','password','email']
        # fields = '__all__'
    
    def getModel(self):
        return self.Meta.model.object.email


class ProfileSer(serializers.ModelSerializer):
    user = UserSerializer()

    def __init__(self, instance=None,customizeFields:list=[],customizeDepth:int=None, **kwargs):
        super().__init__(instance=instance, **kwargs)
        self.Meta.depth = customizeDepth if customizeDepth is not None else None
        for field_name in set(self.fields) - set(customizeFields) : self.fields.pop(field_name) if len(customizeFields) > 0 else None
    

    class Meta:
        depth=0
        model = Profile
        # fields = ['fname', 'lname','user', 'phone', 'coverPhoto','avatar','DOB','document','accountType']
        fields = '__all__'
    
   

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        
        # For Creating user manager is used
        user_obj = UserProfile.objects.create_user(**user_data)
        my_group,created = Group.objects.get_or_create(name='customer')
        my_group.user_set.add(user_obj)

        # for user_da in user_data:
        profile = Profile.objects.create(user=user_obj, **validated_data)

        return profile
    
class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    avatar = serializers.SerializerMethodField(read_only=True)
    coverImage = serializers.SerializerMethodField(read_only=True)

    def __init__(self, instance=None,customizeFields:list=[],customizeDepth:int=None, **kwargs):
        super().__init__(instance=instance, **kwargs)
        self.Meta.depth = customizeDepth if customizeDepth is not None else None
        for field_name in set(self.fields) - set(customizeFields) : self.fields.pop(field_name) if len(customizeFields) > 0 else None

    class Meta:
        depth=0
        model = Profile
        # fields = ['fname', 'lname','user', 'phone', 'coverPhoto','avatar','DOB','document','accountType']
        fields = '__all__'
    
    def get_avatar(self, obj: Profile):
        if obj.avatar:
            return obj.avatar.url[1:]
        else:
            return None   
    def get_coverImage(self, obj: Profile):
        if obj.coverImage:
            return obj.coverImage.url[1:]
        else:
            return None   

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        
        # For Creating user manager is used
        user_obj = UserProfile.objects.create_user(**user_data)
        my_group,created = Group.objects.get_or_create(name='customer')
        my_group.user_set.add(user_obj)

        # for user_da in user_data:
        profile = Profile.objects.create(user=user_obj, **validated_data)

        return profile
    

class AddressSerializer(serializers.ModelSerializer):
    def __init__(self, instance=None,customizeFields:list=[],customizeDepth:int=None, **kwargs):
        super().__init__(instance=instance, **kwargs)
        self.Meta.depth = customizeDepth if customizeDepth is not None else None
        for field_name in set(self.fields) - set(customizeFields) : self.fields.pop(field_name) if len(customizeFields) > 0 else None

    class Meta:
        depth=0
        model=Address
        fields='__all__'

class ProfileSeriL(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields= ['fname', 'lname', 'phone', 'avatar',]

class UserSer(serializers.ModelSerializer):
    class Meta:
        model=UserProfile
        fields=['id','username','email']