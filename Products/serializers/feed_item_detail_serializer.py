import collections
from datetime import datetime
from rest_framework import serializers, exceptions
from General.models import Feed, Review

from General.serilaizers import ImageSerializer, ReviewSerializer
from Products.serializers.attribute_serializer import AttributeSer, ExtraItemSerializer
from Products.serializers.offer_serializer import OfferSerializer
from ..helpers import ProductHelper

from ..models import Collection, Item, Offers, Variant

class FeedItemDetailSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.title", read_only=True)
    coverImage = serializers.SerializerMethodField()
    extra = ExtraItemSerializer(many=True)
    allAttributes = AttributeSer(source="attributes",many=True, read_only=True)
    variant=serializers.SerializerMethodField()
    newPrice = serializers.SerializerMethodField()
    reviewCount=serializers.SerializerMethodField()
    realPrice = serializers.FloatField(source="newPrice", read_only=True)
    offers = serializers.SerializerMethodField()
    # allAttributes = serializers.SerializerMethodField()

    # variant = VariantSerializer(many=True)
    class Meta:
        model = Item
        depth = 3
        fields = [
            "id",
            "title",
            "description",
            "newPrice",
            "slug",
            "avgRating",
            "category",
            "coverImage",
            "extra",
            "reviewCount",
            "variant",
            "realPrice",
            "offers",
            "allAttributes",
        ]
    # def get_allAttributes(self, obj:Item):
    #     return AttributeSer(obj.attributes(), many=True).data
    def get_coverImage(self, obj: Item):
        if obj.coverImage != None:
            return obj.coverImage.file.url[1:]
        else:
            return None   
    def get_newPrice(self, obj:Item):
        offers = Offers.objects.filter(item=obj.id, endAt__gte=datetime.now())
        return ProductHelper.get_offer_product_value(product=obj, offers=list(offers))

    def get_reviewCount(self,obj:Item):
        review=Review.objects.filter(food=obj).count()
        return review
    
    def get_offers(self, obj:Item):
        offers = Offers.objects.filter(item=obj.id, endAt__gte=datetime.now())
        offerData = OfferSerializer(offers, many=True)
        return offerData.data
        
    def get_variant(self,obj:Item):
        variants=obj.variant.all()
        realPrice = 0
        starting=0
        temp=[]
        offers = Offers.objects.filter(item=obj.id, endAt__gte=datetime.now())

        if variants:
            temp.append(variants[0])

            for _ in variants:
                if starting==0:
                    realPrice = _.price
                    starting=ProductHelper.get_varient_product_price(price=_.price, offers=offers)
                elif _.price<starting:
                    realPrice =_.price
                    starting=starting=ProductHelper.get_varient_product_price(price=_.price, offers=offers)
                    
                    temp[0]=_
        
        if len(temp)!=0:
            id=temp[0].id
            variant_instance=Variant.objects.filter(id=id).first()
            if not variant_instance:
                raise exceptions.NotFound("Variant Invalid.")
            var_attributes=variant_instance.items.all()
            attributes={}
            for _ in var_attributes:
                attributes[_.attribute.id]=_.attributeItem.id
            return ({"id":id,"startingPrice":starting,"attribute":attributes, "realPrice":realPrice})
        else:
            return None
            
class ItemCollectionSerializer(serializers.ModelSerializer):
    foods = FeedItemDetailSerializer(many=True)

    class Meta:
        model = Collection
        # depth = 2

        fields = ["id", "title", "description", "foods"]
        # fields='__all__'
class FeedSerializer(serializers.ModelSerializer):
    item=FeedItemDetailSerializer()
    items=FeedItemDetailSerializer(many=True)
    coverImage=ImageSerializer(source='cover_image')
    # gallery=ImageSerializer(source='images',many=True)
    gallery=serializers.SerializerMethodField()
    collection=ItemCollectionSerializer()
    type=serializers.CharField(source='typeName')
    reviews=ReviewSerializer(many=True)

    def __init__(self, instance=None,customizeFields:list=[],customizeDepth:int=None, **kwargs):
        super().__init__(instance=instance, **kwargs)
        self.Meta.depth = customizeDepth if customizeDepth is not None else None
        for field_name in set(self.fields) - set(customizeFields) : self.fields.pop(field_name) if len(customizeFields) > 0 else None
    
    class Meta:
        model=Feed
        fields=['id','type','item','items','coverImage',
                'gallery','collection','reviews']
    
    def to_representation(self, instance):
        result = super(FeedSerializer, self).to_representation(instance)
        return collections.OrderedDict([(key, result[key]) for key in result if (result[key] is not None and result[key] != [])])
    
    def get_coverImage(self, obj: Feed):
        if obj.coverImage:
            return obj.coverImage.url[1:]
        else:
            return None
    def get_gallery(self,obj:Feed):
        if obj.images:
            return [i.get('url') for i in ImageSerializer(obj.images,read_only=True,many=True).data]
        else:
            return None