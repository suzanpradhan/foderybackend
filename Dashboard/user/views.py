from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group, User
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from rest_framework import serializers
from rest_framework.parsers import JSONParser

from CustomUser.models import Profile, UserProfile
from CustomUser.serializer import ProfileSeriL
from .serializer import ProfileSerializer, UserSerializer

class UpdateCreate(LoginRequiredMixin,TemplateView):
    login_url='admin-login'
    template_name='user/update.html'
    def get(self, request,*args, **kwargs):
        try:
            id=kwargs['id']
        except:
            id=None
        if id !=None:
            obj=Profile.objects.get(id=id)
            user=UserProfile.objects.get(id=obj.user.id)
            group=Group.objects.filter(user=user)[0]
            context={
                'data':obj,
                'user':user,
                'group':group.name,
            }

            return render(request, self.template_name,context)
        else:
            return render(request,'user/add.html')
    
    def post(self, request,*args, **kwargs):
        data=request.POST.dict()
        try:
            id=kwargs['id']
        except:
            id=None
        if id!=None:
            data['user']={'username': data['username'],'email': data['email'], 'password': data['password']}
            profile=Profile.objects.get(id=id)
            user=UserProfile.objects.get(id=profile.user.id)

            serializer= ProfileSeriL(profile,data=data,partial=True)
            if serializer.is_valid():
            
                serializer.save()
            else:
                print(serializer.errors)
            serializer2=UserSerializer(user,data=data['user'],partial=True)
            if serializer2.is_valid():
                serializer2.save()
            
            if serializer.is_valid():
                serializer.save()
                my_group = Group.objects.get(name=request.POST.get('groups'))
                user_obj=user
                my_group.user_set.add(user_obj)
            else:
                print(serializer.errors)
            return redirect('user-all')
        else:
            data['user']={'username': data['username'],'email': data['email'], 'password': data['password']}
            serializer= ProfileSerializer(data=data)
            
            if serializer.is_valid():
                serializer.save()
                my_group = Group.objects.get(name=request.POST.get('groups'))
                user_obj=UserProfile.objects.get(username=data['username'],email=data['email'])
                my_group.user_set.add(user_obj)
            else:
                print(serializer.errors)
            return redirect('user-add')

class GetDelete(LoginRequiredMixin,TemplateView):
    login_url='admin-login'
    template_name="user/all.html"

    def get(self, request,*args, **kwargs):
        try:
            id=kwargs['id']
        except:
            id=None
        if id==None:
            obj=Profile.objects.all()
            context={
                'data':obj
            }
            return render(request, self.template_name,context)
        else:
            Profile.objects.filter(id=id).delete()
            return redirect('user-all')
    