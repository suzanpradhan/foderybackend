from django.contrib import admin

from CustomUser.models import UserNotificaiton
from django.utils.html import format_html
from .models import Ads, Feed, City, Country, Review, ShippingClass, ShippingZone, State,MediaFile,File,adsType

admin.site.register(Country)
admin.site.register(State)
admin.site.register(City)
admin.site.register(File)
admin.site.register(Ads)
admin.site.register(adsType)
admin.site.register(ShippingZone)
admin.site.register(ShippingClass)
admin.site.register(Review)
admin.site.register(UserNotificaiton)
admin.site.register(Feed)


class MediaFileAdmin(admin.ModelAdmin):
    list_display = ('title', 'image_file')

    def image_file(self,obj:MediaFile):
        return format_html('<img src="{0}" style="width: 45px; height:45px;" />'.format(obj.file.url))

admin.site.register(MediaFile, MediaFileAdmin)
