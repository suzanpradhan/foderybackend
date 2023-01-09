from rest_framework import serializers, exceptions

from Products.models import OfferChoice, Offers


class OfferSerializer(serializers.ModelSerializer):
    coverImage = serializers.SerializerMethodField()
    typeOfOffer = serializers.SerializerMethodField()

    class Meta:
        model = Offers
        fields = "__all__"

    def get_coverImage(self, obj: Offers):
        if obj.coverImage != None:
            return obj.coverImage.file.url[1:]
        else:
            return None 

    def get_typeOfOffer(self, obj: Offers):
        return OfferChoice(obj.typeOfOffer).name 