from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views
urlpatterns = [
    path('order/all/',views.GetDelete.as_view(),name='order-all'),
    path('order/all/<int:id>/',views.GetDelete.as_view(),name='order-delete'),
    path('order/<int:id>/',views.UpdateCreate.as_view(),name='order-update'),
    path('order/print/<int:id>',views.PrintInvoice.as_view(),name='order-invoice-print'),
    path('order/updateStatus/<int:id>',views.UpdateOrderStatus.as_view(),name='update-order-status'),
    path('order/updatedeliveryBoy/<int:id>',views.UpdateDeliveryBoy.as_view(),name='update-order-delivery-boy'),
]