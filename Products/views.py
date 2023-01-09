from asyncio import exceptions
import re
from typing import ItemsView
from django.http.response import HttpResponseNotFound
from django.shortcuts import render
from django.utils.decorators import method_decorator
from rest_framework import generics, mixins, serializers, exceptions
from rest_framework import response
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.pagination import LimitOffsetPagination
from General.models import MediaFile, Review
from Order.serializer import CartItemSerializer
from Products.helpers import ProductHelper
from Products.serializers.feed_item_detail_serializer import ItemCollectionSerializer
from sweed.decorator import check_token
from sweed import settings
from .models import (
    Collection,
    Extra,
    Favorite,
    Item,
    ItemAttr,
    ItemCategory,
    Nutrition,
    Offers,
    Variant,
    VariantItem,
)
from .serilaizers import (
    CartItemSerializer,
    CategorySerializer,
    CategorytSearch,
    CollectionSearch,
    CollectionSerializer,
    ExtraSerializer,
    FavoriteItemSer,
    FavoriteSerializer,
    FeedItemDetailSerializer,
    ImageSerializer,
    ItemAttrSerializer,
    ItemDetailSerializer,
    ItemSearch,
    ItemSerializer,
    NutritionSerializer,
    OfferSerializer,
)
from rest_framework.request import Request
from datetime import datetime, timedelta, time



class CategoryParentList(generics.ListAPIView):
    queryset = ItemCategory.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        return self.queryset.filter(isParent=True)


class FoodByCat(generics.ListAPIView):
    queryset = Item.objects.all()
    serializer_class = FeedItemDetailSerializer

    def get_queryset(self):
        id = self.kwargs["id"]
        return self.queryset.filter(category=id)


class PromotedFoodList(generics.ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def get_queryset(self):
        return self.queryset.filter(isFeatured=True)

class GetFoodDetail(generics.GenericAPIView):
    def get(self, request, id):
        prodctObj = Item.objects.filter(id=id).first()
        data = ItemDetailSerializer(prodctObj).data
        data['count']=Review.objects.filter(food_id=id).count()
        mayLike,created=Collection.objects.get_or_create(id=18)
        mayLikeSeri=ItemDetailSerializer(mayLike.foods.all(),many=True).data
        data['mayLike']=mayLikeSeri
        return Response(data)


# class GetFood(generics.ListAPIView):
#     queryset = Item.objects.all()
#     serializer_class = ItemSerializer


class CategoryList(generics.ListAPIView):
    pagination_class = None
    queryset = ItemCategory.objects.filter(status=True)
    serializer_class = CategorySerializer

class FeatureCategoryList(generics.ListAPIView):
    queryset = ItemCategory.objects.filter(status=True,isFeatured=True)
    serializer_class = CategorySerializer


class SubCateogryList(generics.GenericAPIView):
    queryset = ItemCategory.objects.all()
    serializer_class = CategorySerializer

    def get(self, request, id):
        queryset = self.queryset.filter(parentId_id=id)
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)


class GetNurtrition(generics.GenericAPIView):
    queryset = Nutrition.objects.all()
    serializer_class = NutritionSerializer

    def get(self, request, id):
        queryset = self.queryset.filter(id=id)
        serializer = self.serializer_class(queryset)
        return Response(serializer.data)


class GetItemAttr(generics.GenericAPIView):
    queryset = ItemAttr.objects.all()
    serializer_class = ItemAttrSerializer

    def get(self, request, id):
        queryset = self.queryset.filter(id=id)
        serializer = self.serializer_class(queryset)
        return Response(serializer.data)


class GetItemCat(generics.GenericAPIView):
    queryset = ItemCategory.objects.all()
    serializer_class = CategorySerializer

    def get(self, request, id):
        queryset = self.queryset.filter(id=id)
        serializer = self.serializer_class(queryset)
        return Response(serializer.data)


@method_decorator(check_token, name="dispatch")
class MakeFavorite(generics.GenericAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

    def post(self, request, *args, **kwargs):
        userID = self.kwargs["user"].id
        product = request.data["product"]
        instance, created = Favorite.objects.get_or_create(
            user_id=userID, product_id=product
        )
        if instance.isLiked == True:
            instance.isLiked = False
        else:
            instance.isLiked = True
        instance.save()
        return Response({"isFavourite": instance.isLiked})


@method_decorator(check_token, name="dispatch")
class CheckFavourite(generics.GenericAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

    def post(self, request, *args, **kwargs):
        userID = self.kwargs["user"].id
        product = request.data["product"]
        isFavourite = Favorite.objects.filter(
            user_id=userID, product_id=product, isLiked=True
        ).exists()

        return Response({"isFavourite": isFavourite})


class CollectionList(generics.ListAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer

    def get(self, request):
        # id=self.kwargs['id']
        queryset = Collection.objects.filter(isFeatured=True)
        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data)


class ItemByColl(generics.ListAPIView):
    queryset = Collection.objects.all()
    serializer_class = ItemCollectionSerializer

    def get_queryset(self):
        id = self.kwargs["id"]
        return self.queryset.filter(slug=id)


@method_decorator(check_token, name="dispatch")
class Search(APIView):
    def post(self, request, *args, **kwargs):
        # data = JSONParser().parse(request)
        data = request.data
        keyword = data["keyword"]
        filter = data["filters"]

        if filter is not None:
            try:
                category = filter["categories"]
                if len(category) == 0:
                    category = None
            except:
                category = None
            if category is None:
                food_queryset = Item.objects.filter(
                    avgRating__gte=filter["rating"],
                    title__contains=keyword,
                    price__range=[
                        filter["price_range"]["from"],
                        filter["price_range"]["to"],
                    ],
                )
            else:
                food_queryset = Item.objects.filter(
                    avgRating__gte=filter["rating"],
                    title__contains=keyword,
                    category__in=category,
                    price__range=[
                        filter["price_range"]["from"],
                        filter["price_range"]["to"],
                    ],
                )

            collection_queryset = Collection.objects.filter(title__contains=keyword)
            category_queryset = ItemCategory.objects.filter(title__contains=keyword)
        else:
            food_queryset = Item.objects.filter(title__contains=keyword)
            collection_queryset = Collection.objects.filter(title__contains=keyword)
            category_queryset = ItemCategory.objects.filter(title__contains=keyword)

        response = Response()
        serializer_context = {"request": request}
        response.data = {
            "food": FeedItemDetailSerializer(
                food_queryset, many=True, context=serializer_context
            ).data,
            "collection": CollectionSearch(collection_queryset, many=True).data,
            "category": CategorytSearch(category_queryset, many=True).data,
        }
        return response

class SearchItemBeta(APIView, LimitOffsetPagination):
    # queryset = Item.objects.all()
    # serializer_class = ItemSerializer

    # def get_queryset(self):
    #     keyword = self.request.query_params.get("keyword")
    #     print(keyword)
    #     queryData = self.queryset
    #     if keyword is not None:
    #         print(len(keyword))
    #         if len(keyword) >= 3:
    #             queryData = queryData.filter(title__contains=keyword)
    #         else:
    #             raise exceptions.NotAcceptable("At least 3 characters is required.")
    #     return queryData
        # productObj = Item.objects.filter(id=self.request.parser_context.get("kwargs").get("id")).first()
        # if productObj is None:
        #     raise exceptions.NotFound("Product Not Found.")
        # else:
        #     return self.queryset.filter(id__in=productObj.gallery.values_list('id', flat=True))
    def post(self, request, format=None):
        keyword = self.request.data["keyword"]
        filters = self.request.data.get("filters")
        queryData = Item.objects.all()
        if keyword is not None and len(keyword) >= 3:
            queryData = queryData.filter(title__icontains=keyword)
        if filters is not None:
            price_range = filters.get("price_range")
            if price_range is not None:
                price_from = price_range.get("from")
                price_to = price_range.get("to")
                if (price_from is not None and price_to is not None):
                    queryData = queryData.filter(price__range=[price_from, price_to])
            rating = filters.get("rating")
            categories = filters.get("categories")
            if (rating is not None):
                queryData = queryData.filter(avgRating__gte=rating)
            if (categories is not None and len(categories) > 0):
                queryData = queryData.filter(category__in=categories)
        results = self.paginate_queryset(queryData, request, view=self)
        serializer = ItemSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)


class GetExtraByGroup(generics.ListAPIView):
    queryset = Extra.objects.all()
    serializer_class = ExtraSerializer

    def get_queryset(self):
        id = self.kwargs["id"]
        return self.queryset.filter(extraGroup=id)


@method_decorator(check_token, name="dispatch")
class GetItemCart(APIView):
    def post(self, request, *args, **kwargs):
        id_list = request.data.get("items")
        queryset = Item.objects.filter(id__in=id_list)
        serializer = CartItemSerializer(queryset, many=True)
        return Response(serializer.data)


@method_decorator(check_token, name="dispatch")
class GetFavItems(APIView):
    def get(self, request, *args, **kwargs):
        query = Favorite.objects.filter(user_id=self.kwargs["user"].id, isLiked=True)
        post_serializer = FavoriteItemSer(query, many=True)
        response = Response()
        response.data = {"data": post_serializer.data}
        return response


@method_decorator(check_token, name="dispatch")
class GetVariantFromAttribute(APIView):
    def post(self, request, *args, **kwargs):
        items=[]
        for (k,v) in request.data.items():
            attribute=int(k)
            attributeItem=v
            item = VariantItem.objects.filter(
            attribute_id=attribute, attributeItem=attributeItem 
            ).first()
            if item is None:
                return HttpResponseNotFound("Variant Not Found.")
            items.append(item.id)
        # attribute = request.data.get("attribute")
        # attributeItem = request.data.get("attributeItem")
        query=None

        for _ in items:
            if query is not None:
                query = query.filter(items=_)
            else:
                query=Variant.objects.filter(items=_)

        query=query.first()
        
        if query is None:
            return HttpResponseNotFound("Variant Not Found.")
        tempVarientPrice = query.price
        offers = Offers.objects.filter(item=query.items.first().attribute.item.id, endAt__gte=datetime.now())
        tempVarientPrice = ProductHelper.get_varient_product_price(price=tempVarientPrice, offers=offers)
        response = Response()
        response.data = {"id": query.id, "price": tempVarientPrice}
        return response

@method_decorator(check_token, name="dispatch")
class GetOffers(APIView):
    def get(self, request, *args, **kwargs):
        today = datetime.now().date()
        todayTime = datetime.combine(today, time())
        query = Offers.objects.filter(endAt__gte=todayTime)
        offer_serializer = OfferSerializer(query, many=True)
        response = Response()
        response.data = {"data": offer_serializer.data}
        return response


# GET FOOD GALLERY
@method_decorator(check_token, name="dispatch")
class GetFoodGallery(generics.ListAPIView):
    queryset = MediaFile.objects.all()
    serializer_class = ImageSerializer

    def get_queryset(self):
        productObj = Item.objects.filter(id=self.request.parser_context.get("kwargs").get("id")).first()
        if productObj is None:
            raise exceptions.NotFound("Product Not Found.")
        else:
            return self.queryset.filter(id__in=productObj.gallery.values_list('id', flat=True))
