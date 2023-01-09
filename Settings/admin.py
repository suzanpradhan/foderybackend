from django.contrib import admin
from .models import *

admin.site.register(appSettings)
admin.site.register(FAQ)
admin.site.register(FAQCategory)
admin.site.register(Coupons)
admin.site.register(Currency)
admin.site.register(Tax)
admin.site.register(User_Coupons)
admin.site.register(AppNotificaiton)
admin.site.register(AppNotificaitonUser)
admin.site.register(Reward)
admin.site.register(RewardCollection)
admin.site.register(RewardCoupon)
admin.site.register(OrderInfo)