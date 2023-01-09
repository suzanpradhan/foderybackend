from rest_framework import serializers, exceptions

from Products.models import Attribute, AttributeItem, Extra

class AttributeItemSer(serializers.ModelSerializer):
    coverImage = serializers.SerializerMethodField()
    class Meta:
        model = AttributeItem
        fields = "__all__"
    
    def get_coverImage(self, obj: AttributeItem):
        if obj.coverImage != None:
            return obj.coverImage.file.url[1:]
        else:
            return None   

class AttributeSer(serializers.ModelSerializer):
    items=AttributeItemSer(many=True, read_only=True)
    id = serializers.IntegerField(source="pk", read_only=True)
    title = serializers.SerializerMethodField()
    class Meta:
        model = Attribute
        fields = ("id", "title", "items")

    def get_title(self, obj:Attribute):
        return obj.name.title if obj.name else ""


class ExtraItemSerializer(serializers.ModelSerializer):
    coverImage = serializers.SerializerMethodField()

    class Meta:
        model = Extra
        fields = ["id", "title", "price", "coverImage", "extraGroup", "description"]
    
    def get_coverImage(self, obj: Extra):
        if obj.coverImage != None:
            return obj.coverImage.file.url[1:]
        else:
            return None   