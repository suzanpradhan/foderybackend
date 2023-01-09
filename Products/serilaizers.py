from datetime import datetime
from tokenize import endpats
from unicodedata import category
from rest_framework import serializers
from rest_framework import exceptions
from General.models import MediaFile, Review
from General.serilaizers import ImageSerializer
from Products.helpers import ProductHelper
from Products.serializers.attribute_serializer import AttributeItemSer, AttributeSer, ExtraItemSerializer
from Products.serializers.offer_serializer import OfferSerializer
from .serializers.feed_item_detail_serializer import FeedItemDetailSerializer

from .models import (
    Attribute,
    Collection,
    Extra,
    Favorite,
    Item,
    ItemAttr,
    ItemCategory,
    Nutrition,
    OfferChoice,
    Offers,
    Variant,
    VariantItem,
)


class CategorySerializer(serializers.ModelSerializer):
    coverImage = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()

    class Meta:
        model = ItemCategory
        fields = "__all__"

    def get_coverImage(self, obj: ItemCategory):
        if obj.coverImage != None:
            return obj.coverImage.file.url[1:]
        else:
            return None   

    def get_count(self, obj: ItemCategory):
        return Item.objects.filter(category=obj.pk).count()


class ItemSerializer(serializers.ModelSerializer):
    coverImage = serializers.SerializerMethodField()
    categoryName = serializers.SerializerMethodField()
    def __init__(
        self,
        instance=None,
        customizeFields: list = [],
        customizeDepth: int = None,
        concentrated_product=False,
        **kwargs
    ):
        super().__init__(instance=instance, **kwargs)
        self.Meta.depth = customizeDepth if customizeDepth is not None else None
        for field_name in set(self.fields) - set(customizeFields):
            self.fields.pop(field_name) if len(customizeFields) > 0 else None

        if concentrated_product:
            self.Meta.fields = (
                ["id", "title", "coverImage", "weight", "itemAttribute"],
            )
    def get_categoryName(self, obj: Item):
        if obj.category != None:
            return obj.category.title
        else:
            return ""   
    def get_coverImage(self, obj):
        if obj.coverImage != None:
            return obj.coverImage.file.url[1:]
        else:
            return None   

    class Meta:
        depth = 0
        model = Item
        fields = "__all__"


class NurtitionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nutrition
        fields = ["title", "quantity", "unit"]



class VariantAttributeSer(serializers.ModelSerializer):
    items=AttributeItemSer(many=True, read_only=True)
    class Meta:
        model = Attribute
        fields = ["id","title", 'items']


class VariantItemSerializer(serializers.ModelSerializer):
    attribute=VariantAttributeSer(many=False)
    attributeItem=AttributeItemSer(many=False)
    class Meta:
        model = VariantItem
        fields = "__all__"

class VariantSerializer(serializers.ModelSerializer):
    items=VariantItemSerializer(many=True, read_only=True)
    class Meta:
        model = Variant
        fields = '__all__'





class NutritionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nutrition
        fields = "__all__"


class ItemAttrSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemAttr
        fields = "__all__"


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = "__all__"


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        exclude = ["foods"]


class HomePageItemSerializer(serializers.ModelSerializer):
    coverImage = serializers.SerializerMethodField()
    category = serializers.CharField(source="category.title", read_only=True)

    class Meta:
        model = Item
        fields = [
            "id",
            "title",
            "newPrice",
            "description",
            "coverImage",
            "category",
        ]
    
    def get_coverImage(self, obj: Item):
        if obj.coverImage != None:
            return obj.coverImage.file.url[1:]
        else:
            return None   

# class ImageSerializer(serializers.ModelSerializer):
#     url=serializers.SerializerMethodField()
#     class Meta:
#         model=MediaFile
#         fields=['url']
#     def get_url(self, obj: MediaFile):
#         if obj.file:
#             return obj.file.url[1:]
#         else:
#             return None

# class ImageSerializer(serializers.ModelSerializer):
#     url=serializers.SerializerMethodField()
#     class Meta:
#         model=MediaFile
#         fields="__all__"
#     def get_url(self, obj: MediaFile):
#         if obj.file:
#             return obj.file.url[1:]
#         else:
#             return None



class ItemDetailSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.title", read_only=True)
    coverImage = serializers.SerializerMethodField()
    nutritions = NurtitionItemSerializer(many=True)
    extra = ExtraItemSerializer(many=True)
    allAttributes = AttributeSer(source="attributes",many=True, read_only=True)
    related_product=HomePageItemSerializer(source='relatedProduct',many=True)
    variant=serializers.SerializerMethodField()
    gallery=serializers.SerializerMethodField()
    reviewCount=serializers.SerializerMethodField()
    newPrice = serializers.SerializerMethodField()
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
            "variant",
            "slug",
            "weight",
            "itemAttribute",
            "category",
            "coverImage",
            "nutritions",
            "extra",
            "allAttributes",
            "gallery",
            "avgRating",
            'reviewCount',
            "related_product",
            'offers',
            'realPrice'
        ]
    # def get_allAttributes(self, obj:Item):
    #     return AttributeSer(obj.attributes(), many=True).data
    def get_coverImage(self, obj: Item):
        if obj.coverImage != None:
            return obj.coverImage.file.url[1:]
        else:
            return None
    def get_variant(self,obj:Item):
        variants=obj.variant.all()
        starting=0
        temp=[]
        offers = Offers.objects.filter(item=obj.id, endAt__gte=datetime.now())

        if variants:
            temp.append(variants[0])

            for _ in variants:
                if starting==0:
                    starting=ProductHelper.get_varient_product_price(price=_.price, offers=offers)
                elif _.price<starting:
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
            return ({"id":id,"startingPrice":starting,"attribute":attributes})
        else:
            return None
    def get_gallery(self,obj:Item):
        if obj.gallery:
            return [i.get('url') for i in ImageSerializer(obj.gallery,read_only=True,many=True).data]
        else:
            return None
    def get_reviewCount(self,obj:Item):
        review=Review.objects.filter(food=obj).count()
        return review

    def get_newPrice(self, obj:Item):
        tempNewPrice = 0
        offers = Offers.objects.filter(item=obj.id, endAt__gte=datetime.now())
        tempNewPrice = ProductHelper.get_offer_product_value(product=obj, offers=list(offers))
        return tempNewPrice
    def get_offers(self, obj:Item):
        offers = Offers.objects.filter(item=obj.id, endAt__gte=datetime.now())
        offerData = OfferSerializer(offers, many=True)
        return offerData.data







class ItemSearch(serializers.ModelSerializer):
    coverImage = serializers.SerializerMethodField()
    categoryName = serializers.SerializerMethodField()
    class Meta:
        model = Item
        fields = ["id", "title", "coverImage", "newPrice", "categoryName"]
    
    def get_coverImage(self, obj: Item):
        if obj.coverImage != None:
            return obj.coverImage.file.url[1:]
        else:
            return None   
    def get_categoryName(self, obj: Item):
        if obj.category != None:
            return obj.category.title
        else:
            return None   


class CollectionSearch(serializers.ModelSerializer):
    coverImage = serializers.SerializerMethodField()

    class Meta:
        model = Collection
        fields = ["id", "title", "coverImage"]
    
    def get_coverImage(self, obj: Item):
        if obj.coverImage != None:
            return obj.coverImage.file.url[1:]
        else:
            return None   


class CategorytSearch(serializers.ModelSerializer):
    coverImage = serializers.SerializerMethodField()

    class Meta:
        model = ItemCategory
        fields = ["id", "title", "coverImage"]
    
    def get_coverImage(self, obj: Item):
        if obj.coverImage != None:
            return obj.coverImage.file.url[1:]
        else:
            return None   


class ExtraSerializer(serializers.ModelSerializer):
    coverImage = serializers.SerializerMethodField()

    class Meta:
        model = Extra
        fields = ["id", "title", "coverImage"]
    
    def get_coverImage(self, obj: Item):
        if obj.coverImage != None:
            return obj.coverImage.file.url[1:]
        else:
            return None   


class CartItemSerializer(serializers.ModelSerializer):
    coverImage = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = ["id", "title", "coverImage", "newPrice"]
        
    def get_coverImage(self, obj: Item):
        if obj.coverImage != None:
            return obj.coverImage.file.url[1:]
        else:
            return None   

class QuickOrderCartItemSerializer(serializers.ModelSerializer):
    coverImage = serializers.SerializerMethodField()
    varientId = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = ["id", "title", "coverImage", "newPrice", "varientId"]
        
    def get_coverImage(self, obj: Item):
        if obj.coverImage != None:
            return obj.coverImage.file.url[1:]
        else:
            return None   

    def get_varientId(self, obj: Item):
        if obj.variant != None and obj.variant.all().count() > 0:
            return obj.variant.first().id
        else:
            return None

# class FeedItemDetailSerializer(serializers.ModelSerializer):
#     category = serializers.CharField(source="category.title", read_only=True)
#     coverImage = serializers.SerializerMethodField()
#     extra = ExtraItemSerializer(many=True)
#     allAttributes = AttributeSer(source="attributes",many=True, read_only=True)
#     variant=serializers.SerializerMethodField()

#     # allAttributes = serializers.SerializerMethodField()

#     # variant = VariantSerializer(many=True)
#     class Meta:
#         model = Item
#         depth = 3
#         fields = [
#             "id",
#             "title",
#             "description",
#             "newPrice",
#             "slug",
#             "avgRating",
#             "category",
#             "coverImage",
#             "extra",
#             "variant",
#             "allAttributes",
#         ]
#     # def get_allAttributes(self, obj:Item):
#     #     return AttributeSer(obj.attributes(), many=True).data
#     def get_coverImage(self, obj: Item):
#         if obj.coverImage != None:
#             return obj.coverImage.file.url[1:]
#         else:
#             return None   
    
#     def get_variant(self,obj:Item):
#         variants=obj.variant.all()
#         starting=0
#         temp=[]

#         if variants:
#             temp.append(variants[0])

#             for _ in variants:
#                 if starting==0:
#                     starting=_.price
#                 elif _.price<starting:
#                     starting=_.price
                    
#                     temp[0]=_
        
#         if len(temp)!=0:
#             id=temp[0].id
#             variant_instance=Variant.objects.filter(id=id).first()
#             if not variant_instance:
#                 raise exceptions.NotFound("Variant Invalid.")
#             var_attributes=variant_instance.items.all()
#             attributes={}
#             for _ in var_attributes:
#                 attributes[_.attribute.id]=_.attributeItem.id
#             return ({"id":id,"startingPrice":starting,"attribute":attributes})
#         else:
#             return None
class FavoriteItemSer(serializers.ModelSerializer):
    product = FeedItemDetailSerializer(data="product")

    class Meta:
        model = Favorite
        fields = "__all__"

