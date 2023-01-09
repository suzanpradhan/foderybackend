from django.contrib import admin

from CustomUser.models import Refer
from .models import *

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(DeliverAddress)
admin.site.register(Discount)
admin.site.register(Transaction)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(ExtraOrder)