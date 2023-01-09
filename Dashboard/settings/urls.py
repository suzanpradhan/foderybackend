from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views
urlpatterns = [
    path('faq/all/',views.GetDeleteFAQ.as_view(),name='faq-all'),
    path('faq/all/<int:id>/',views.GetDeleteFAQ.as_view(),name='faq-delete'),
    path('faq/',views.UpdateCreateFAQ.as_view(),name='faq-add'),
    path('faq/<int:id>/',views.UpdateCreateFAQ.as_view(),name='faq-update'),
    path('coupon/all/',views.GetDeleteCoupon.as_view(),name='coupon-all'),
    path('coupon/all/<int:id>/',views.GetDeleteCoupon.as_view(),name='coupon-delete'),
    path('coupon/',views.UpdateCreateCoupon.as_view(),name='coupon-add'),
    path('coupon/<int:id>/',views.UpdateCreateCoupon.as_view(),name='coupon-update'),
    path('general/',views.GeneralView.as_view(),name='general'),
    path('appSettings/',views.AppSetingView.as_view(),name='app-setting'),
    path('tax/',views.TaxView.as_view(),name='tax'),
    path('deleteShippingRule/<int:id>/',views.DeleteShippingRule.as_view(),name='ship-delete'),
    path('addShippingRule/',views.UpdateCreateShipping.as_view(),name='ship-add'),
    path('addShippingRule/<int:id>/',views.UpdateCreateShipping.as_view(),name='ship-update'),
    path('deleteShippingZone/<int:id>/',views.DeleteShippingZone.as_view(),name='zone-delete'),
    path('addShippingZone/',views.UpdateCreateShippingZone.as_view(),name='zone-add'),
    path('addShippingZone/<int:id>/',views.UpdateCreateShippingZone.as_view(),name='zone-update'),

]