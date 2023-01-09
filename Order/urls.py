from django.contrib import admin
from django.urls import path
from django.urls.conf import include

from .views import AcceptOrder, CashOnDeliveryPaid, DestroyCartItem, GetAssignedNewOrders, GetCompletedOrder, GetEachDeliveryOrder, GetPendingOrder, GetUpdateDestroyCart, GetUserOrder, ReOrder, RejectOrder, RetriveOrder, TemporaryDeliver, VerifyDelivery, changeQuantityCart, createCart, createOrder, deleteExtraCart, getCart, GetDeliveringOrders, GetDeliveredOrders, AddMassCart
urlpatterns = [
    path('addOrder/', createOrder.as_view()),
    path('reOrder/', ReOrder.as_view()),
    path('userOrder/', GetUserOrder.as_view()),
    path('getOrder/<int:id>', RetriveOrder.as_view()),
    path('getCart/', getCart.as_view()),
    path('addCart/', createCart.as_view()),
    path('add_mass_cart/', AddMassCart.as_view()),
    path('change_item_quantity/', changeQuantityCart.as_view()),
    path('delete_extra/', deleteExtraCart.as_view()),
    path('get_pending_order/', GetPendingOrder.as_view()),
    path('get_completed_order/', GetCompletedOrder.as_view()),
    path('getUpdateDeleteCart/<int:id>/', GetUpdateDestroyCart.as_view()),
    path('deleteCart/', DestroyCartItem.as_view()),
    path('get_new_assigned_order', GetAssignedNewOrders.as_view()),
    path('accept_order/', AcceptOrder.as_view()),
    path('reject_order/', RejectOrder.as_view()),
    path('verify_delivery/', VerifyDelivery.as_view()),
    path('cash_on_delivery_paid', CashOnDeliveryPaid.as_view()),
    path('get_delivering_order/', GetDeliveringOrders.as_view()),
    path('get_delivered_order/', GetDeliveredOrders.as_view()),
    path('get_each_delivery_order/<int:id>', GetEachDeliveryOrder.as_view()),
    path('temporary_deliver', TemporaryDeliver.as_view())
    ]