
from django.core.exceptions import ValidationError
from django.http import HttpResponseNotAllowed, response
from django.http.response import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.utils.decorators import method_decorator
from rest_framework import exceptions, generics, serializers
import bcrypt
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from CustomUser.orderplaced import get_order_placed_html
from Order.models import Cart, CartItem, DeliverAddress, Discount, ExtraOrder, Order, OrderStatus
from CustomUser.models import Address, Refer, UserProfile
from Order.serializer import (
    CartSerializer,
    DeliveryBoyNewOrdersSerializer,
    OrderAddressSerializer,
    OrderItemSerializer,
    OrderReturnSerializer,
    OrderSerialzier,
    ReturnOrderSerialzier,
    UserOrderSerializer,
)
from Products.helpers import ProductHelper
from Products.models import Extra, Item, Offers, Variant
from Products.serilaizers import CartItemSerializer
from Settings.models import Coupons, OrderInfo, Reward, Tax, User_Coupons, appSettings
from django.forms.models import model_to_dict
from django.db.models import Q
from fodery.decorator import check_token
from django.core.mail.message import EmailMultiAlternatives
import jwt
from fodery import settings
import datetime



@method_decorator(check_token, name="dispatch")
class createOrder(APIView):

    def orderUpdateToEmail(self, order: Order): 
        subject = "Fodery - New Order Has Been Placed!"
        message = "New Order Has Been Placed!"
        html_context=get_order_placed_html(order=order)
        recepient = settings.ORDER_UPDATES_EMAIL
        msg=EmailMultiAlternatives(subject,message,settings.EMAIL_HOST_USER,[recepient])
        msg.attach_alternative(html_context,"text/html")
        msg.send()

    def post(self, request, *args, **kwargs):

        data = JSONParser().parse(request)

        if data["userAddress"] == None:
            return HttpResponseBadRequest("User Address is required.")

        # Initial Values
        totalAmount = 0
        totalWeight = 0
        extraPrice = 0

        # Getting or Creating Order Address
        address = data["userAddress"]
        address_obj = Address.objects.filter(id=address).first()
        if address_obj is None:
            raise exceptions.NotFound("Address doesn't exist.")
        addressdata = model_to_dict(address_obj)
        addressSerializer = OrderAddressSerializer(data=addressdata)
        if addressSerializer.is_valid():
            address_obj = addressSerializer.save()
            data["DeliveryAddress"] = address_obj.id
        else:
            raise ValidationError("Address Incorrect")

        # Querying each product
        # try:
        for key, item in enumerate(data['listProduct']):
            # Initial Values for OrderProducts
            item_price = 0
            total_price = 0
            extra_price = 0
            today = datetime.datetime.now()
            todayTime = datetime.datetime.combine(today, datetime.time())
            offers = Offers.objects.filter(item_id=item["item"], endAt__gte=today)
            print(item["item"])
            print(offers)
            # Price calculation syncing with Variant / Offers
            if item["variant"] and Variant.objects.filter(id=item["variant"]).exists():
                variant = Variant.objects.filter(id=item["variant"]).first()
                item_price = ProductHelper.get_varient_product_price(price=variant.price, offers=list(offers))
            else:
                itemObj = Item.objects.filter(id=item["item"]).first()
                item_price = ProductHelper.get_offer_product_value(product=itemObj, offers=list(offers))
            item_price = item_price * item["quantity"]
            print(item_price)
            # Extra Items Price calculation
            if item["extras"]:
                for extra in item["extras"]:
                    extra_obj_query = Extra.objects.filter(id=extra)
                    if extra_obj_query.exists():
                        order_extra_obj = ExtraOrder.objects.create(
                            extra=extra_obj_query.first()
                        )
                        extra_price += ProductHelper.get_extra_sync_offer_price(extra=extra_obj_query.first(), offers=list(offers))
            data['listProduct'][key]["extras_price"] = extra_price
            data["extraAmount"] = extraPrice
            data['listProduct'][key]["item_price"] = item_price
            total_price = item_price + extra_price
            data['listProduct'][key]["total_price"] = total_price
            totalAmount += item_price + extra_price
        # except:
        #     address_obj.delete()
        #     raise exceptions.NotAcceptable("Order price calculation failed.")
            


            # try:
            #     extra = _["extras"]
            # except:
            #     extra=None
            
            # if extra:
            #     for _ in extra:
            #         extra_obj = Extra.objects.get(id=_)
            #         order_extra_obj = ExtraOrder.objects.create(
            #             extra=extra_obj
            #         )
            #         # temp_extra.append(order_extra_obj.id)
            #         extraPrice += extra_obj.price

                # data["listProduct"]["extras"] = temp_extra

                
        
        #Product Item Validation

        listProduct = data["listProduct"]
        print(listProduct)
        serializer = OrderItemSerializer(data=listProduct, many=True)
        try:
            if serializer.is_valid():
                order_items_obj = serializer.save()  # Getting Order Item and serializing it
            else:
                address_obj.delete()
                raise exceptions.NotAcceptable(serializer.errors)
        except:
            address_obj.delete()
            raise exceptions.NotAcceptable("Products are not valid.")

        # for obj in model_obj:  # Getting total price from Items Sent
        #     if obj.variant:
        #         offers = Offers.objects.filter(item=obj.id)
        #         eachPrice = ProductHelper.get_varient_product_price(price=obj.variant.price, offers=list(offers))
        #     else:
        #         offers = Offers.objects.filter(item=obj.id)
        #         eachPrice = ProductHelper.get_offer_product_value(product=obj.item, offers=list(offers))
        #     totalAmount += eachPrice * float(obj.quantity)
            # totalWeight += (obj.item.weight) * float(obj.quantity)

        

        data["amount"] = totalAmount
        tempList = []
        for _ in order_items_obj:
            tempList.append(_.id)
        data["items"] = tempList



        # else:
        #     address = data["orderAddress"]
        #     address_obj = Address.objects.filter(id=address).first()
        #     if address_obj is None:
        #         raise exceptions.NotFound("Address doesn't exist.")
        #     addressdata = model_to_dict(address_obj)
        #     addressSerializer = OrderAddressSerializer(data=addressdata)
        #     if addressSerializer.is_valid():
        #         address_obj = addressSerializer.save()
        #         data["DeliveryAddress"] = address_obj.id
        #     else:
        #         raise ValidationError("Address Incorrect")

        # Creating and serailizing Coupon objects
        try:
            coupon=data["coupon"]
        except:
            coupon=None
       
        if coupon:
            couponObj = Coupons.objects.filter(id=coupon).first()
            if couponObj is not None:
                user_coupon_obj,created=User_Coupons.objects.get_or_create(user=self.kwargs['user'],coupon=couponObj)
                if not created:
                    if user_coupon_obj.used:
                        raise exceptions.PermissionDenied("Coupon already used.")
                if coupon.isReward:
                    coupon.status=False
                    coupon.save()
                if not couponObj.isReward:    
                    user_coupon_obj.used=True
                    user_coupon_obj.save()
                if couponObj.unitType == "1":
                    data["couponAmount"] = couponObj.discount * totalAmount
                else:
                    data["couponAmount"] = couponObj.discount
        else:
            data["couponAmount"] = 0
        


        # Creating and serailizing Discount objects
        # discountObj=Discount.objects.get(id=1)
        # if discountObj.unitType=='1':
        #     data['discountAmount']=discountObj.amount*totalAmount
        # else:
        #     data['discountAmount']=discountObj.amount

        data["discountAmount"] = 0

        # Shipping Rule

        shippingPrice = 0
        # shippingZoneObj = ShippingZone.objects.filter(city=address_obj.city).first()
        # if shippingZoneObj is None:
        #     raise exceptions.NotFound("Shipping rule doesn't exist.")
        # for _ in shippingZoneObj.shippingClass.all().order_by("priority"):
        #     if _.type == 2:
        #         if _.start <= totalAmount and _.end >= totalAmount:
        #             shippingPrice += _.price
        #             break
        #     if _.type == 1:
        #         if _.start <= totalWeight and _.end >= totalWeight:
        #             shippingPrice += _.price
        #             break

        data["shipAmount"] = shippingPrice

        totalAmount = totalAmount - data["couponAmount"] - data["discountAmount"]
        setting=appSettings.objects.get(id=1)

        amountForReward = round((totalAmount + extraPrice) * (setting.cashBackPercentage / 100))

        # taxAmount = Tax.objects.get(id=1)
        # data["taxAmount"] = (taxAmount.value / 100) * totalAmount
        taxAmount = 0
        data["cashBackReward"] = amountForReward
        # totalAmount = totalAmount + data["taxAmount"]

        data["user"] = self.kwargs["user"].id

        # totalAmount=totalAmount+shippingPrice
        data["grandAmount"] = totalAmount
        

        # Checking if the total amount sent from front end is valid
        # if data['total'] != None:
        # if totalAmount==data['total']:
        # print(data)
        orderSerilize = OrderSerialzier(data=data, many=False)
        if orderSerilize.is_valid():
            model_obj = orderSerilize.save()
            current_cart, status=Cart.objects.get_or_create(user=self.kwargs['user'])
            current_cart.items.set([])

            #Bill No. Receipt No.
            bill_instance,created=OrderInfo.objects.get_or_create(id=1)
            bill_instance.billNo+=1
            bill_instance.receiptNo+=1
            bill_instance.save()

            model_obj.billNo=bill_instance.billNo
            model_obj.receiptNo=bill_instance.receiptNo
            model_obj.save()
            # self.orderUpdateToEmail(order=model_obj)

            # for Cashback Reward
            # rewardInts,created=Reward.objects.get_or_create(user=self.kwargs['user'])
            # rewardInts.points += amountForReward
            # rewardInts.save()
            address_ser = OrderReturnSerializer(address_obj).data

            return Response(
                {
                    "orderId":model_obj.id,
                    "status": "Order Created Successfully.",
                    "billNo":bill_instance.billNo,
                    "receiptNo":bill_instance.receiptNo,
                    "data": ReturnOrderSerialzier(
                        Order.objects.get(id=model_obj.id)
                    ).data,
                    "address": address_ser,
                    "cashBack": amountForReward
                }
            )

        # # Coupon use
        #     if User_Coupons.objects.filter(coupon=couponObj,user_id=self.kwargs['user'].id).exists():
        #         coupon_user_obj=User_Coupons.objects.get(coupon=couponObj,user_id=data['user'])
        #         coupon_user_obj.used=True
        #         coupon_user_obj.save()

        #         rewardPoints=totalAmount*(2/100)
        #         reward_obj=Reward.objects.get_or_create(user_id=data['user'])
        #         reward_obj.points+=rewardPoints
        #         reward_obj.save()

        else:
            #    return Response({
            #         'status':'error',
            #         'message':'Order not created.'
            #     })
            print(orderSerilize.errors)
            return HttpResponseBadRequest("Server Error")
            # else:
            #     raise ValidationError("Please don't tamper with the product prices.")
        # else:
        #     orderSerilize=OrderSerialzier(data=data,many=False)
        #     if orderSerilize.is_valid():
        #         model_obj=orderSerilize.save()

        #         # Coupon use
        #         coupon_user_obj=User_Coupons.objects.get(coupon=couponObj,user_id=data['user'])
        #         coupon_user_obj.used=True
        #         coupon_user_obj.save()

        #         # # return_data=orderSerilize.validated_data[0]
        #         # return_data=orderSerilize.validated_data

        #         # return_data['DeliveryAddress']=model_to_dict(return_data['DeliveryAddress'])
        #         # return_data['coupon']=model_to_dict(return_data['coupon'])
        #         # return_data['discount']=model_to_dict(return_data['discount'])
        #         # return_data['currency']=model_to_dict(return_data['currency'])
        #         # return_data['tax']=model_to_dict(return_data['tax'])
        #         # return_data['user']=model_to_dict(return_data['user'])
        #         # # return_data['extras']=model_to_dict(return_data['extras'])
        #         # # return_data['items']=model_to_dict(return_data['items'])
        #         # print(return_data)
        #         return Response({

        #             'status':'Order Created Successfully.',
        #             'data':ReturnOrderSerialzier(Order.objects.get(id=model_obj.id)).data,
        #             'address':addressSerializer.data,

        #         })

        # return Response(serializer.validated_data)


@method_decorator(check_token, name="dispatch")
class createCart(APIView):
    def post(self, request, *args, **kwargs):
        _ = request.data
        quantity= _.get("quantity")
        variant=_.get("variant")
        item=_.get("item")
        extra=_.get("extra")
        
        cart_obj,created=Cart.objects.get_or_create(user_id=self.kwargs["user"].id)

        if variant:
            item_obj,created=cart_obj.items.get_or_create(variant_id=variant,items_id=item)
        else:
            item_obj,created=cart_obj.items.get_or_create(items_id=item)
        if created:
            item_obj.quantity=quantity
            print(True)
        else:
            item_obj.quantity+=quantity
        for id in extra:
            obj=Extra.objects.get(id=id)
            item_obj.extra.add(obj)

        item_obj.save()
        cart_obj.items.add(item_obj.id)
        cart_obj.save()

        response=Response()
        response.data=CartSerializer(cart_obj).data
        return response

@method_decorator(check_token, name="dispatch")
class AddMassCart(APIView):
    def post(self, request, *args, **kwargs):
        cart_obj,created=Cart.objects.get_or_create(user_id=self.kwargs["user"].id)
        for _ in request.data.get("products"):
            quantity= _.get("quantity")
            variant=_.get("variant")
            item=_.get("item")
            extra=_.get("extra")

            if variant:
                item_obj,created=cart_obj.items.get_or_create(variant_id=variant,items_id=item)
            else:
                item_obj,created=cart_obj.items.get_or_create(items_id=item)
            if created:
                item_obj.quantity=quantity
                print(True)
            else:
                item_obj.quantity+=quantity
            if extra:
                for id in extra:
                    obj=Extra.objects.get(id=id)
                    item_obj.extra.add(obj)
            item_obj.save()
            cart_obj.items.add(item_obj.id)
            cart_obj.save()

        response=Response()
        response.data=CartSerializer(cart_obj).data
        return response

@method_decorator(check_token, name="dispatch")
class getCart(APIView):
    def get(self, request, *args, **kwargs):
        query=Cart.objects.filter(user=self.kwargs["user"]).first()
        if query is None:
            return HttpResponseNotFound("Cart not found.")
        response=Response()
        response.data=CartSerializer(query,many=False).data
        return response

@method_decorator(check_token, name="dispatch")
class changeQuantityCart(APIView):
    def post(self, request, *args, **kwargs):
        cartItem=request.data.get("id")
        quantity=request.data.get("quantity")
        if cartItem is None or quantity is None:
            return HttpResponseBadRequest("Invalid cart or quantity.")
        cartItem_obj=CartItem.objects.filter(id=cartItem).first()
        if cartItem_obj is None:
            return HttpResponseNotFound("Cart not found.")
        cartItem_obj.quantity=quantity
        cartItem_obj.save()
        return HttpResponse("Success.")

@method_decorator(check_token, name="dispatch")
class deleteExtraCart(APIView):
    def post(self, request, *args, **kwargs):

        cartItem=request.data.get("id")
        id=request.data.get("extra")

        if cartItem is None or id is None:
            return HttpResponseBadRequest("Invaid cart or quantity.")
        cartItem_obj=CartItem.objects.filter(id=cartItem).first()

        if cartItem_obj is None:
            return HttpResponseNotFound("Cart not found.")
        
        extra_obj=Extra.objects.filter(id=id).first()

        if extra_obj is None:
            return HttpResponseNotFound("Invalid Extra.")

        extras=list(cartItem_obj.extra.all())

        extras.remove(extra_obj)

        print(extras)
        cartItem_obj.extra.set(extras)

        return HttpResponse("Success")
        
        
@method_decorator(check_token, name="dispatch")
class RetriveOrder(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = ReturnOrderSerialzier
    lookup_field = "id"


@method_decorator(check_token, name="dispatch")
class GetUpdateDestroyCart(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    lookup_field = "id"

    def post(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

@method_decorator(check_token, name="dispatch")
class DestroyCartItem(APIView):
    def post(self, request, *args, **kwargs):
        id=request.data.get('id')
        cart=Cart.objects.filter(user=kwargs['user']).first()
        if cart is None:
            raise exceptions.NotFound("Cart invalid.")
        cartitem_obj=CartItem.objects.filter(id=id).first()
        if cartitem_obj is None:
            raise exceptions.NotFound("Cart Item not found.")
        if cartitem_obj not in cart.items.all():
            raise exceptions.NotFound("Cart Item invalid.")
        
        cartitem_obj.delete()

        return Response("Success")


@method_decorator(check_token, name="dispatch")
class GetAssignedOrders(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = DeliveryBoyNewOrdersSerializer

    def get_queryset(self):
        return self.queryset.filter(
            deliveryPerson_id=self.kwargs["user"].id, status=OrderStatus.pending.value
        )


@method_decorator(check_token, name="dispatch")
class AcceptOrder(APIView):
    def post(self, request, *args, **kwargs):
        userID = self.kwargs["user"].id
        orderID = request.data.get("orderID")

        if userID and orderID:
            try:
                order = Order.objects.get(id=orderID, deliveryPerson_id=userID)
                order.status = 3
                order.save()

                return Response("You accepted the order.")
            except:
                raise Exception("Order is not valid.")

        else:
            raise Exception("UserID and OrderID required.")


@method_decorator(check_token, name="dispatch")
class RejectOrder(APIView):
    def post(self, request, *args, **kwargs):
        userID = self.kwargs["user"].id

        orderID = request.data.get("orderID")

        if userID and orderID:
            try:
                order = Order.objects.get(id=orderID, deliveryPerson_id=userID)
                order.status = 1
                order.deliveryPerson = None
                order.save()

                return Response("You rejected the order.")
            except:
                raise Exception("Order is not valid.")

        else:
            raise Exception("UserID and OrderID required.")

@method_decorator(check_token, name="dispatch")
class CashOnDeliveryPaid(APIView):
    def post(self, request, *args, **kwargs):
        orderID = request.data.get('orderId')

        if orderID:
            try:
                order = Order.objects.get(id=orderID)
            except:
                order = None
            if order is not None:
                if order.isPaid == False:
                    order.isPaid = True
                    order.save()
                    return Response("Order status has changed to paid.")
                else:
                    return HttpResponseBadRequest("Order has already paid.")
            else:
                raise Exception("Order doesn't exist.")
        else:
            return HttpResponseNotAllowed("Order Id and Order Key is required.")
@method_decorator(check_token, name="dispatch")
class VerifyDelivery(APIView):
    def post(self, request, *args, **kwargs):
        orderID = request.data.get("orderId")
        orderKey = request.data.get("orderKey")

        if orderID and orderKey:
            try:
                order = Order.objects.get(order_number=orderKey)
            except:
                order = None

            if order is not None:
                if order.status != OrderStatus.delivered.value:
                    if order.isPaid == True:
                        order.status = OrderStatus.delivered.value
                        order.isTransactionConfirmed = True
                        order.deliveredAt = datetime.datetime.now()
                        order.save()

                        # Cash Back
                        if order.cashBackReward and order.cashBackReward > 0:
                            rewardInts,created=Reward.objects.get_or_create(user=self.kwargs['user'])
                            rewardInts.points += order.cashBackReward
                            rewardInts.save()

                        # Refer
                        refer_obj=Refer.objects.filter(referedTo=order.user).first()
                        if refer_obj:
                            if not refer_obj.status:
                                setting=appSettings.objects.get(id=1)
                                referedBy,created=Reward.objects.get_or_create(user=refer_obj.referedBy)
                                referedTo,created=Reward.objects.get_or_create(user=refer_obj.referedTo)
                                referedBy.points+=setting.referReward
                                referedTo.points+=setting.referReward
                                refer_obj.status=True
                                refer_obj.save()
                                referedBy.save()
                                referedTo.save()
                        return Response("Delivery Successful.")
                    else:
                        return HttpResponseBadRequest("Payment has not been processed.")
                else:
                    return HttpResponseBadRequest("Order has already delivered.")
            else:
                raise Exception("Order doesn't exist.")
        else:
            raise Exception("UserID, OrderID and identifier required.")


@method_decorator(check_token, name="dispatch")
class GetUserOrder(APIView):
    def get(self, request, *args, **kwargs):
        query = Order.objects.filter(user=self.kwargs["user"])
        return Response(UserOrderSerializer(query, many=True).data)


@method_decorator(check_token, name="dispatch")
class GetPendingOrder(APIView):
    def get(self, request, *args, **kwargs):
        query = Order.objects.filter(~Q(status=4), user=self.kwargs["user"])
        return Response(UserOrderSerializer(query, many=True).data)


@method_decorator(check_token, name="dispatch")
class GetCompletedOrder(APIView):
    def get(self, request, *args, **kwargs):
        query = Order.objects.filter(user=self.kwargs["user"], status=4)
        return Response(UserOrderSerializer(query, many=True).data)


@method_decorator(check_token, name="dispatch")
class ReOrder(APIView):
    def post(self, request, *args, **kwargs):
        order_obj = Order.objects.filter(id=request.data.get("order")).first()
        if order_obj is None:
            raise exceptions.NotFound("Order Not Found.")
        delivery_obj = DeliverAddress.objects.filter(
            id=order_obj.DeliveryAddress.id
        ).first()
        if delivery_obj is None:
            raise exceptions.NotFound("Address Not Found.")
        extras = order_obj.extras.all()
        items = order_obj.items.all()
        order_obj.id = None
        order_obj.save()
        order_obj.extras.set(extras)
        order_obj.items.set(items)

        return Response(
            {
                "status": "Order Created Successfully.",
                "data": ReturnOrderSerialzier(order_obj).data,
                "address": OrderReturnSerializer(delivery_obj).data,
            }
        )


@method_decorator(check_token, name="dispatch")
class GetAssignedNewOrders(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = DeliveryBoyNewOrdersSerializer

    def get_queryset(self):
        return self.queryset.filter(
            deliveryPerson_id=self.kwargs["user"].id, status=OrderStatus.pending.value
        )

@method_decorator(check_token, name="dispatch")
class GetDeliveringOrders(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = DeliveryBoyNewOrdersSerializer

    def get_queryset(self):
        return self.queryset.filter(
            deliveryPerson_id=self.kwargs["user"].id, status=OrderStatus.delivering.value
        )


@method_decorator(check_token, name="dispatch")
class GetDeliveredOrders(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = DeliveryBoyNewOrdersSerializer

    def get_queryset(self):
        return self.queryset.filter(
            deliveryPerson_id=self.kwargs["user"].id, status=OrderStatus.delivered.value
        )

@method_decorator(check_token, name="dispatch")
class GetEachDeliveryOrder(APIView):
    def get(self, request, id, *args, **kwargs):
        try:
            orderObj = Order.objects.filter(id=id).first()
            if (orderObj):
                data = DeliveryBoyNewOrdersSerializer(orderObj).data
                return Response(data=data)
            else:
                return HttpResponseNotFound("Order Not Found")
        except:
            return HttpResponseNotFound("Order Not Found")



@method_decorator(check_token, name="dispatch")
class TemporaryDeliver(APIView):
    def post(self, request, *args, **kwargs):
        orderID = request.data.get('orderId')

        if orderID:
            try:
                order = Order.objects.get(id=orderID)
            except:
                order = None
            if order is not None:
                if order.status == OrderStatus.delivering.value:
                    order.status = OrderStatus.delivered.value
                    order.save()
                    return Response("Temporary Deliver Success.")
                else:
                    return HttpResponseBadRequest("Order not in delivering mode.")
            else:
                raise Exception("Order doesn't exist.")
        else:
            return HttpResponseNotAllowed("Order Id a is required.")