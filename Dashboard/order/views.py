from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group, User
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from rest_framework import serializers
from rest_framework.parsers import JSONParser
from CustomUser.models import UserProfile

from Order.models import Order
from Products.helpers import ProductHelper
from Products.models import Offers

class GetDelete(LoginRequiredMixin,TemplateView):
    login_url='admin-login'
    template_name='order/all.html'

    def get(self, request,*args, **kwargs):
        try:
            id=kwargs['id']
        except:
            id=None
        if id==None:
            obj=Order.objects.all()
            context={
                'data':obj,
                'data1':obj
            }
            return render(request, self.template_name,context)
        else:
            Order.objects.filter(id=id).delete()
            return redirect('order-all')

class UpdateCreate(LoginRequiredMixin,TemplateView):
    login_url='admin-login'
    template_name='order/update.html'

    def get(self, request,*args, **kwargs):
        try:
            id=kwargs['id']
        except:
            id=None

        if id !=None:
            group=UserProfile.objects.filter(groups__name='delivery')
            
            obj=Order.objects.get(id=id)
            items = []
            for i in obj.items.all():
                tempItem = {}
                itemPrice = 0
                extraPrice = 0
                tempItem["name"] = i.item.title
                tempItem["quantity"] = i.quantity
                offers = Offers.objects.filter(item_id = i.item.id, endAt__gte=datetime.now())
                if (i.variant): 
                    tempItem["variant"] = i.variant.readable_name()
                    itemPrice += ProductHelper.get_varient_product_price(i.variant.price, offers=offers)
                else:
                    tempItem["variant"] = None
                    itemPrice += ProductHelper.get_offer_product_value(product=i.item, offers=offers)
                itemPrice 
                if i.extras.count() > 0: 
                    tempItem["extras"] = i.extras
                    for i in i.extras.all():
                        extraPrice += i.price
                tempItem["itemPrice"] = itemPrice
                tempItem["extraPrice"] = extraPrice
                tempItem["itemTotal"] = itemPrice + extraPrice
                items.append(tempItem)
            context={
            'data':obj,
            'delivery':group,
            'items': items
            }
            return render(request, self.template_name,context)
        else:
            return HttpResponse('Error')
    
    def post(self, request,*args, **kwargs):
        try:
            id=kwargs['id']
        except:
            id=None

        if id is not None:
            status=request.POST.get('status')
            delivery=request.POST.get('delivery')
            print(delivery)
            order=Order.objects.get(id=id)
            order.status=status
            order.deliveryPerson_id=delivery
            order.save()
            
            return redirect('order-all')

class PrintInvoice(LoginRequiredMixin,TemplateView):
    login_url='admin-login'
    template_name='order/invoice.html'

    def get(self, request, id,*args, **kwargs):
        group=UserProfile.objects.filter(groups__name='delivery')
        
        obj=Order.objects.get(id=id)
        context={
        'data':obj,
        'delivery':group
        }
        return render(request, self.template_name,context)

class UpdateOrderStatus(LoginRequiredMixin, TemplateView):
    login_url='admin-login'

    def post(self, request, id,*args, **kwargs ):
        status=request.POST.get('status')
        orderObj = Order.objects.get(id=id)
        orderObj.status = status
        orderObj.save()

        return redirect('order-update', id=orderObj.id)


class UpdateDeliveryBoy(LoginRequiredMixin, TemplateView):
    login_url='admin-login'

    def post(self, request, id,*args, **kwargs ):
        deliveryBoy=request.POST.get('deliveryBoy')
        orderObj = Order.objects.get(id=id)
        orderObj.deliveryPerson_id = deliveryBoy
        orderObj.save()

        return redirect('order-update', id=orderObj.id)