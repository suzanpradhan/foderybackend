from django.contrib import admin

from QuickOrder.views import QuickOrder
from .models import *

class FoodTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'status')

admin.site.register(FoodType, FoodTypeAdmin)

class DietAdmin(admin.ModelAdmin):
    list_display = ('name', 'status')

admin.site.register(Diet, DietAdmin)

class PeopleGroupTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'numberOfPeople')

admin.site.register(PeopleGroupType, PeopleGroupTypeAdmin)
