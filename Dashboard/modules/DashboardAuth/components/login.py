from this import s
from time import process_time_ns
from django.http import HttpResponse, request
from django.shortcuts import redirect, render
from django.contrib.auth import login, logout
from django_unicorn.components import UnicornView
from django.contrib import messages

from CustomUser.models import UserProfile

class LoginView(UnicornView):
    email = ""
    password = ""

    def mount(self):
        print(self.request.user.is_authenticated)
        if (self.request.user.is_authenticated):
            return redirect('home')
        

    def login_submit(self):
        
        if (self.email is None) or (self.password is None):
            messages.error(self.request, "Email and Password required.")
        user = UserProfile.objects.filter(email=self.email).first()
        if user is None:
            self.call("fireError", "User not found.")
        elif not user.check_password(self.password):
            self.call("fireError", "Wrong password.")
        elif not user.groups.filter(name="lords").exists():
            self.call("fireError", "Not Authorized.")
        elif not user.is_active or not user.is_staff:
            self.call("fireError", "Your account has been blocked. Please contact an administrator.")
        else:
            login(self.request,user)
            return redirect('home')