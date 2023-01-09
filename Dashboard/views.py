from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from CustomUser.models import UserProfile

class HomePage(TemplateView):
    template_name = "dashboard/dashboard.html"
    login_url='admin-login'
    # def get(self,request):
    #     return render(request,'dashboard/dashboard.html')

class Logout(TemplateView):
    def get(self,request):
        logout(request)
        return redirect('admin-login')