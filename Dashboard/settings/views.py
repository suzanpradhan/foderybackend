from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group, User
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from rest_framework import serializers
from rest_framework.parsers import JSONParser
from CustomUser.models import UserProfile
from General.models import City, ShippingClass, ShippingZone

from Order.models import Order
from Settings.models import FAQ, Coupons, Currency, FAQCategory, Tax, appSettings

class GetDeleteFAQ(LoginRequiredMixin,TemplateView):
    login_url='admin-login'
    template_name='settings/faq.html'

    def get(self, request,*args, **kwargs):
        try:
            id=kwargs['id']
        except:
            id=None
        if id==None:
            obj=FAQ.objects.all()
            categories=FAQCategory.objects.all()

            context={
                'data':obj,
                'categories':categories

            }
            return render(request, self.template_name,context)
        else:
            FAQ.objects.filter(id=id).delete()
            return redirect('faq-all')

class UpdateCreateFAQ(LoginRequiredMixin,TemplateView):
    login_url='admin-login'
    template_name='settings/faq.html'

    def get(self, request,*args, **kwargs):

        data=FAQ.objects.all()
        categories=FAQCategory.objects.all()
        context={
        'faq':data,
        'categories':categories
        }
        return render(request, self.template_name,context)
       
    
    def post(self, request,*args, **kwargs):
        try:
            id=kwargs['id']
        except:
            id=None
        category=request.POST.get('category')
        question=request.POST.get('question')
        answer=request.POST.get('answer')

        if id is None:
            faq_obj=FAQ.objects.create(faqCategory_id=category,question=question,answer=answer)
            return redirect('faq-all')
        else:
            faq_obj=FAQ.objects.filter(id=id).first()
            
            if faq_obj is None:
                return HttpResponse("FAQ not found.")
            
            if category:
                faq_obj.faqCategory_id=category
            
            if question:
                faq_obj.question=question

            if answer:
                faq_obj.answer=answer
            
            faq_obj.save()

            return redirect('faq-all')


class GetDeleteCoupon(LoginRequiredMixin,TemplateView):
    login_url='admin-login'
    template_name='settings/coupon.html'

    def get(self, request,*args, **kwargs):
        try:
            id=kwargs['id']
        except:
            id=None
        if id==None:
            obj=Coupons.objects.filter(isReward=False)

            context={
                'data':obj,

            }
            return render(request, self.template_name,context)
        else:
            FAQ.objects.filter(id=id).delete()
            return redirect('coupon-all')

class UpdateCreateCoupon(LoginRequiredMixin,TemplateView):
    login_url='admin-login'
    template_name='settings/coupon.html'

    def get(self, request,*args, **kwargs):

        data=FAQ.objects.all()
        categories=FAQCategory.objects.all()
        context={
        'faq':data,
        'categories':categories
        }
        return render(request, self.template_name,context)
       
    
    def post(self, request,*args, **kwargs):
        try:
            id=kwargs['id']
        except:
            id=None
        code=request.POST.get('code')
        description=request.POST.get('description')
        discount=request.POST.get('discount')
        unit=request.POST.get('unit')
        status=request.POST.get('status')
        expire=request.POST.get('expire')

        if id is None:
            coupon_obj=Coupons.objects.create(code=code,description=description,discount=discount,unitType=unit,expiresAt=expire)
            return redirect('coupon-all')
        else:
            coupon_obj=Coupons.objects.filter(id=id).first()
            
            if coupon_obj is None:
                return HttpResponse("Coupon not found.")
            
            if code:
                coupon_obj.code=code
            
            if description:
                coupon_obj.description=description

            if discount:
                coupon_obj.discount=discount

            if unit:
                coupon_obj.unitType=unit

            if status:
                coupon_obj.status=status

            if expire:
                coupon_obj.expiresAt=expire
            
            coupon_obj.save()

            return redirect('coupon-all')

class GeneralView(LoginRequiredMixin,TemplateView):
    login_url='admin-login'
    template_name='settings/general.html'

    def get(self, request,*args, **kwargs):
        appsetting=appSettings.objects.filter(id=1).first()            
        tax=Tax.objects.get(id=1)
        currencies=Currency.objects.all()
        shipping_obj=ShippingClass.objects.all().order_by('priority')
        zone=ShippingZone.objects.all()
        city=City.objects.all()
        if appSettings:
            context={
                'data':zone,
                'setting':appsetting,
                'tax':tax,
                'currencies':currencies,
                'shippingclass':shipping_obj,
                'cities':city
            }
        else:
            context={
                'tax':tax,
                'currencies':currencies
            }
        return render(request, self.template_name,context)
        

class AppSetingView(LoginRequiredMixin,TemplateView):
    login_url='admin-login'
    
    def post(self, request,*args, **kwargs):
        data=request.POST.dict()
        data.pop('csrfmiddlewaretoken')
        appsetting_obj=appSettings.objects.filter(id=1).first()
        if appsetting_obj:
            appsetting_obj.delete()
        appsetting_obj=appSettings.objects.create(id=1,**data)
        return redirect('general')

class TaxView(LoginRequiredMixin,TemplateView):
    login_url='admin-login'
    
    def post(self, request,*args, **kwargs):
        tax=request.POST.get('tax')
        currency=request.POST.get('currency')
        tax_obj=Tax.objects.filter(id=1).first()
        if tax_obj:
            tax_obj.delete()
        tax_obj=Tax.objects.create(id=1,value=tax,isDefault=True)
        setting_obj=appSettings.objects.filter(id=1).first()
        if setting_obj:
            setting_obj.currency_id=currency
            setting_obj.save()
        return redirect('general')

class DeleteShippingRule(LoginRequiredMixin,TemplateView):
    login_url='admin-login'
    def post(self, request,*args, **kwargs):
        id=kwargs['id']
        ShippingClass.objects.get(id=id).delete()
        return redirect('general')

class UpdateCreateShipping(LoginRequiredMixin,TemplateView):
    login_url='admin-login'
    def post(self, request,*args, **kwargs):
        try:
            id=kwargs['id']
        except:
            id=None
        data=request.POST.dict()
        data.pop('csrfmiddlewaretoken')
        if id is None:
            ShippingClass.objects.create(**data)
            return redirect('general')
        else:
            ShippingClass.objects.filter(id=id).update(**data)

            return redirect('general')

class DeleteShippingZone(LoginRequiredMixin,TemplateView):
    login_url='admin-login'
    def post(self, request,*args, **kwargs):
        id=kwargs['id']
        ShippingZone.objects.get(id=id).delete()
        return redirect('general')

class UpdateCreateShippingZone(LoginRequiredMixin,TemplateView):
    login_url='admin-login'
    def post(self, request,*args, **kwargs):
        try:
            id=kwargs['id']
        except:
            id=None
        data=request.POST.dict()
        # shippingList=request.POST.getlist('shippingClass')
        # shippingList=[int(x) for x in shippingList]
        # data['shippingClass']=shippingList
        data.pop('csrfmiddlewaretoken')
        data.pop('shippingClass')
        if id is None:
            ship=ShippingZone(**data)
            ship.save()
            ship.shippingClass.set(request.POST.getlist('shippingClass'))
            return redirect('general')
        else:
            ship=ShippingZone.objects.filter(id=id)
            ship.update(**data)
            ship.first().shippingClass.set(request.POST.getlist('shippingClass'))
            return redirect('general')
