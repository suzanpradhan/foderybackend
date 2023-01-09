from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group, Permission, User
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from CustomUser.models import UserProfile

class UpdateCreate(LoginRequiredMixin,TemplateView):
    login_url='admin-login'
    template_name='roles/update.html'

    def get(self, request,*args, **kwargs):
        try:
            id=kwargs['id']
        except:
            id=None
        context={
            'users':UserProfile.objects.all(),
            'perms':Permission.objects.all()
            }

        if id !=None:
            obj=Group.objects.get(id=id)
            context={
            'data':obj,
            'users':UserProfile.objects.all(),
            'perms':Permission.objects.all()
            }
            return render(request, self.template_name,context)
        else:
            return render(request,'roles/add.html',context)
        
    def post(self, request,*args, **kwargs):
        try:
            id=kwargs['id']
        except:
            id=None
        
        if id!=None:
            role=request.POST.get('role')
            perms=request.POST.getlist('perm')
            users=request.POST.getlist('user')

            group=Group.objects.get(id=id)

            for _ in perms:
                group.permissions.add(Permission.objects.get(id=_))
            for _ in users:
                group.user_set.add(UserProfile.objects.get(id=_))


            return render(request,'roles/all.html')
        else:
            role=request.POST.get('role')
            perms=request.POST.getlist('perm')
            users=request.POST.getlist('user')
            print(role)

            group=Group.objects.create(name=role)
            for _ in perms:
                group.permissions.add(Permission.objects.get(id=_))
            for _ in users:
                group.user_set.add(UserProfile.objects.get(id=_))

            return redirect('role-all')

class GetDelete(LoginRequiredMixin,TemplateView):
    login_url='admin-login'
    template_name="roles/all.html"

    def get(self, request,*args, **kwargs):
        try:
            id=kwargs['id']
        except:
            id=None
        if id==None:
            obj=Group.objects.all()
            context={
                'data':obj
            }
            return render(request, self.template_name,context)
        else:
            Group.objects.filter(id=id).first().delete()
            return redirect('role-all')

class Get(LoginRequiredMixin,TemplateView):
    login_url='admin-login'
    template_name="roles/perm_user.html"

    def get(self, request,*args, **kwargs):
        permissions = Permission.objects.filter(group=request.user.groups.name)
        context={
                'data':permissions
            }
        print(context)
        return render(request, self.template_name,context)