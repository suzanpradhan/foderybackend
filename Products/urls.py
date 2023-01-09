from django.contrib import admin
from django.urls import path
from django.urls.conf import include

from .views import CategoryParentList,CategoryList, CheckFavourite, CollectionList, FeatureCategoryList, FoodByCat, GetExtraByGroup, GetFavItems, GetFoodDetail, GetFoodGallery, GetItemAttr, GetItemCart, GetItemCat, GetNurtrition, GetOffers, GetVariantFromAttribute, ItemByColl, MakeFavorite, PromotedFoodList, Search, SearchItemBeta,SubCateogryList

urlpatterns = [
    path('parent_category/', CategoryParentList.as_view()),
    path('category/', CategoryList.as_view()),
    path('featured_category/', FeatureCategoryList.as_view()),
    path('get_sub_category/<int:id>', SubCateogryList.as_view()),
    path('promoted_food/', PromotedFoodList.as_view()),
    # path('get_food/', GetFood.as_view()),
    path('get_food/<int:id>/', GetFoodDetail.as_view()),
    path("get_food_gallery/<int:id>",GetFoodGallery.as_view()),
    path('get_nutrition/<int:id>/', GetNurtrition.as_view()),
    path('get_item_attr/<int:id>/', GetItemAttr.as_view()),
    path('get_item_cat/<int:id>/', GetItemCat.as_view()),
    path('get_item_by_cat/<int:id>/', FoodByCat.as_view()),
    path('make_favorite/', MakeFavorite.as_view()),
    path('check_favorite/', CheckFavourite.as_view()),
    path('get_favorite/', GetFavItems.as_view()),
    path('get_collection/', CollectionList.as_view()),
    path('get_item_by_coll/<str:id>/', ItemByColl.as_view()),
    path('get_extra_by_group/<int:id>/', GetExtraByGroup.as_view()),
    path('search/', Search.as_view()),
    path('query_cart_item/',GetItemCart.as_view()),
    path('get_variant/',GetVariantFromAttribute.as_view()),
    path('get_offers', GetOffers.as_view()),
    path('search_product', SearchItemBeta.as_view()),
]
