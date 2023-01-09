from datetime import datetime
from re import L
from rest_framework import serializers
from CustomUser.models import Address
from CustomUser.serializer import AddressSerializer
from Products.helpers import ProductHelper

from Products.models import Item, Offers, Variant
from Products.serilaizers import ExtraItemSerializer, ItemSerializer
from .models import Cart, CartItem, DeliverAddress, ExtraOrder, Order, OrderItem, OrderStatus

class AddressOrder(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ["streetAdd1"]

class CartVariant(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    class Meta:
        model=Variant
        fields=["id","price","title"]

    def get_title(self,obj:Variant):
        title=[]
        for _ in obj.items.all():
            title.append(_.attributeItem.title)
        return title


class CartItemSerializer(serializers.ModelSerializer):
    extra=ExtraItemSerializer(many=True)
    cart_id = serializers.CharField(source="id")
    item_id = serializers.CharField(source="items.id")
    title = serializers.CharField(source="items.title")
    category=serializers.SerializerMethodField()
    coverImage = serializers.SerializerMethodField()
    newPrice = serializers.SerializerMethodField()
    
    variant=CartVariant()
    class Meta:
        model=CartItem
        fields=["cart_id","item_id","title","category","quantity","newPrice","coverImage","variant","extra"]
        depth=2
    
    def get_coverImage(self, obj: CartItem):
        return obj.items.coverImage.file.url[1:]

    def get_category(self, obj: CartItem):
        return obj.items.category.title if obj.items.category else None


    def get_newPrice(self, obj: CartItem):
        price = 0
        if obj.variant:
            offers = Offers.objects.filter(item=obj.items.id, endAt__gte=datetime.now())
            if offers:
                price += ProductHelper.get_varient_product_price(price=obj.variant.price, offers=offers)
            else:
                price += obj.variant.price
        else:
            offers = Offers.objects.filter(item=obj.items.id, endAt__gte=datetime.now())
            if offers:
                price += ProductHelper.get_offer_product_value(product=obj.items, offers=offers)
            else:
                price += obj.items.newPrice
        if obj.extra:
            for i in obj.extra.all():
                price += i.price
        price = price * obj.quantity
        return price


class CartSerializer(serializers.ModelSerializer):
    items=CartItemSerializer(many=True)
    class Meta:
        model = Cart
        fields = "__all__"


class orderExtraSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtraOrder
        fields = "__all__"


class OrderSerialzier(serializers.ModelSerializer):
    extras = orderExtraSerializer(data="extras", read_only=True, many=True).initial_data

    class Meta:
        model = Order
        # depth=1
        exclude = ["transaction"]


class ReturnOrderItem(serializers.ModelSerializer):
    name = serializers.CharField(source="item.title", read_only=True)
    # price = serializers.CharField(source="item.newPrice", read_only=True)
    # variant=CartVariant(many=False)
    variant_name = serializers.SerializerMethodField()
    category= serializers.CharField(source="item.category.title", read_only=True)
    coverImage_url = serializers.SerializerMethodField()
    extras = ExtraItemSerializer(many=True)
    extra_label = serializers.SerializerMethodField()
    item_price = serializers.FloatField(read_only=True)
    extras_price = serializers.FloatField(read_only=True)
    total_price = serializers.FloatField(read_only=True)
    id = serializers.SerializerMethodField()

    # coverImage_url = serializers.CharField(source="item.coverImage.file.url", read_only=True)
    class Meta:
        model = OrderItem
        fields = ["id","category","quantity", "name","coverImage_url","variant_name","extras", "item_price", "extras_price", "total_price", "extra_label"]

    def get_coverImage_url(self, obj: OrderItem):
        return obj.item.coverImage.file.url[1:]
    
    def get_id(self, obj: OrderItem):
        return  obj.item.id if obj.item else None

    def get_variant_name(self, obj:OrderItem):
        return obj.get_variant_name()
    
    def get_extra_label(self, obj:OrderItem):
        tempLabel = ""
        for i, element in enumerate(obj.extras.all()):
            if (i == (obj.extras.count() - 1)):
                tempLabel = tempLabel + element.title
            else:
                tempLabel = tempLabel + element.title + ", "
        return tempLabel


class ReturnOrderSerialzier(serializers.ModelSerializer):
    items = ReturnOrderItem(data="items", many=True)
    address = AddressOrder(source="DeliveryAddress", read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "amount",
            "billNo",
            "receiptNo",
            "createdAt",
            "taxAmount",
            "shipAmount",
            "extraAmount",
            "couponAmount",
            "discountAmount",
            "grandAmount",
            "items",
            "address",
            "order_number",
        ]


class OrderAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliverAddress
        fields = "__all__"


class OrderReturnSerializer(serializers.ModelSerializer):
    state = serializers.CharField(source="state.title")
    country = serializers.CharField(source="country.title")
    city = serializers.CharField(source="city.title")

    class Meta:
        model = DeliverAddress
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):
    def __init__(
        self,
        instance=None,
        customizeFields: list = [],
        customizeDepth: int = None,
        concentrated_product=False,
        data=...,
        **kwargs
    ):
        super().__init__(instance=instance, data=data, **kwargs)
        self.Meta.depth = customizeDepth if customizeDepth is not None else None
        for field_name in set(self.fields) - set(customizeFields):
            self.fields.pop(field_name) if len(customizeFields) > 0 else None

        if concentrated_product:
            self.fields["item"] = serializers.SerializerMethodField(
                "get_concentrated_product"
            )

    def get_concentrated_product(self, obj: OrderItem):
        return ItemSerializer(
            obj.item,
            customizeFields=[
                "id",
                "title",
                "description",
                "coverImage",
                "extra",
                "weight",
                "itemAttribute",
            ],
        ).data

    class Meta:
        depth = 0
        model = OrderItem
        fields = "__all__"


class DeliveryBoyNewOrdersSerializer(serializers.Serializer):
    orderId = serializers.IntegerField(read_only=True, source="id")
    orderKey = serializers.CharField(read_only=True, source="order_number")
    customerName = serializers.CharField(
        read_only=True, source="user.profile_full_name"
    )
    customerEmail = serializers.CharField(read_only=True, source="user.email")
    customerPhone = serializers.SerializerMethodField("phoneNumber")
    customerAvatar = serializers.CharField(read_only=True, source="user.profile.avatar")
    totalAmount = serializers.FloatField(source="grandAmount")
    location = AddressSerializer(source="DeliveryAddress", customizeDepth=1)
    products = OrderItemSerializer(
        source="items",
        many=True,
        customizeFields=["quantity", "item", "id"],
        customizeDepth=1,
        concentrated_product=True,
    )
    isPaid = serializers.BooleanField(read_only=True)
    isTransactionConfirmed = serializers.BooleanField(read_only=True)
    deliveredAt = serializers.DateTimeField(read_only=True)

    def phoneNumber(self, obj: Order):
        if obj.user.profile_exists():
            return obj.user.profile().phone
        else:
            return None


class ItemImageSerializer(serializers.ModelSerializer):
    coverImage_url = serializers.CharField(
        source="item.coverImage.file.url", read_only=True
    )

    class Meta:
        model = Item
        fields = ["coverImage_url"]


class UserOrderSerializer(serializers.ModelSerializer):
    # items = ItemImageSerializer(data="items", read_only=True, many=True)
    items = serializers.SerializerMethodField()
    # status=serializers.CharField(source='status.name',read_only=True)
    address = AddressOrder(source="DeliveryAddress", read_only=True)
    status = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "id",
            "order_number",
            "status",
            "couponAmount",
            "discountAmount",
            "grandAmount",
            "createdAt",
            "items",
            "address",
        ]

    def get_status(self, obj: Order):
        return OrderStatus(obj.status).name
    
    def get_items(self,obj:Order):
        return [i.get('coverImage_url')[1:] for i in ItemImageSerializer(obj.items,read_only=True,many=True).data]
