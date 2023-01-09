from rest_framework import serializers
from CustomUser.models import UserNotificaiton
from General.models import Ads, Country, MediaFile, Review, State, City

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'
    
class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = '__all__'
    
class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'
    
class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ads
        fields = '__all__'

class MediaFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaFile
        fields = '__all__'  

class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.profile_full_name", read_only=True)
    avatar = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Review
        fields = '__all__'  
        
    
    def get_avatar(self, obj:Review):
        if obj.user.profile_exists():
            try:
                return obj.user.profile().avatar.url[1:]
            except:
                return ""
        else:
            return None
        # return obj.user.profile().avatar.url if obj.user.profile_exists() != False else None


class UserNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserNotificaiton
        fields = '__all__'  

class ImageSerializer(serializers.ModelSerializer):
    url=serializers.SerializerMethodField()
    class Meta:
        model=MediaFile
        fields=['url']
    def get_url(self, obj: MediaFile):
        if obj.file:
            return obj.file.url[1:]
        else:
            return None

