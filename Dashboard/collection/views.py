from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group, Permission, User
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from Products.models import Collection, Extra, Item, ItemAttr, ItemCategory, Nutrition

class GetDelete(LoginRequiredMixin,TemplateView):
    login_url='admin-login'
    template_name="products/all.html"

    def get(self, request,*args, **kwargs):
        try:
            id=kwargs['id']
        except:
            id=None
        if id==None:
            obj=Item.objects.all()
            context={
                'data':obj
            }
            return render(request, self.template_name,context)
        else:
            Item.objects.filter(id=id).delete()
            return redirect('product-all')
 
class UpdateCreate(LoginRequiredMixin,TemplateView):
    login_url='admin-login'
    template_name='collection/update.html'

    def get(self, request,*args, **kwargs):
        
        try:
            id=kwargs['id']
        except:
            id=None
        
        if id is None:
            # collection_obj=Collection.objects.get(id=id)
            food=Item.objects.all()
            context={
                # 'collection':collection_obj,
                'foods':food,
            }
            return render(request,'collection/add.html',context)
        # else:
        #     collection_obj=Collection.objects.get(id=id)
        #     food=Food.objects.filter()
        #     context={
        #         'data':data,
        #         'nutritions':nutritions,
        #         'extras':extras,
        #         'itemcat':itemcat,
        #     }
        #     return render(request,'products/update.html',context)

class AddNutrition(LoginRequiredMixin,TemplateView):
    login_url='admin-login'
    def post(self, request,*args, **kwargs):
        title=request.POST.get("title")
        quantity=int(request.POST.get("quantity"))

        if title is None or quantity is None:
            return HttpResponseBadRequest("Title and Quantity both are required.")
        
        nurtrition_obj=Nutrition.objects.create(title=title,quantity=quantity)

        return HttpResponse("Success")