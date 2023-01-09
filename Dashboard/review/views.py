from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group, Permission, User
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from General.models import Review
from Products.models import Extra, Item, ItemAttr, ItemCategory, Nutrition

class Get(LoginRequiredMixin,TemplateView):
    login_url='admin-login'
    template_name="review/all.html"

    def get(self, request,*args, **kwargs):
        try:
            id=kwargs['id']
        except:
            id=None
        if id!=None:
            obj=Review.objects.filter(food_id=id)
            context={
                'data':obj
            }
            return render(request, self.template_name,context)
        else:
            return HttpResponse('Not found')


class Delete(LoginRequiredMixin,TemplateView):
    login_url='admin-login'
    template_name="review/all.html"

    def get(self, request,*args, **kwargs):
        try:
            id=kwargs['id']
        except:
            id=None
        if id!=None:
            review_obj=Review.objects.filter(id=id).first()
            id=review_obj.food.id
            review_obj.delete()
            return redirect('http://127.0.0.1:8000/dashboard/review/all/'+str(id))
        else:
            return HttpResponse('Not found')

class Update(LoginRequiredMixin,TemplateView):
    login_url='admin-login'
    template_name="review/all.html"

    def post(self, request,id,*args, **kwargs):
        isFeatured=request.POST.get("isfeatured")
        print(isFeatured)
        review_obj=Review.objects.filter(id=id).first()
        if review_obj is None:
            return HttpResponse("Not Found")
        review_obj.isFeatured=isFeatured
        review_obj.save()
        return redirect('http://127.0.0.1:8000/dashboard/review/all/'+str(review_obj.food.id))

class ReviewTemplate(LoginRequiredMixin,TemplateView):
    login_url='admin-login'
    template_name="review/foods.html"

    def get(self, request,*args, **kwargs):
        obj=Item.objects.all()
        temp_output=[]
        for _ in obj:
            count=Review.objects.filter(food=_).count()
            temp_dict=_.__dict__
            temp_dict['count']=count
            temp_dict['url']=_.coverImage.file.url
            temp_output.append(temp_dict)
        context={
            'data':temp_output
        }
        return render(request, self.template_name,context)