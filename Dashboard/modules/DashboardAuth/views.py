from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django_unicorn.components import UnicornView
from CustomUser.models import UserProfile

# # Create your views here.
# class Login(UnicornView):
#     template_name = "templates/login.html"
#     name = "Login"
#     def get(self,request):
#         return render(request,'login.html')
#     def post(self,request):
#         data=request.POST.dict()
#         email=request.POST.get('email')
#         password=request.POST.get('password')
#         print(email,password)

#         if (email is None) or (password is None):
#             return HttpResponse("Email and Password required")
        
#         user = UserProfile.objects.filter(email=email).first()
#         if user is None:
#             return HttpResponse("user not found")
#         elif not user.check_password(password):
#             return HttpResponse("wrong password")
#         elif not user.groups.filter(name="lords").exists():
#             return HttpResponse("Not Authorized.")
#         else:
#             login(request,user)
#             return redirect('home')
#         return redirect('login')

class Login(TemplateView):
    template_name = "login_index.html"