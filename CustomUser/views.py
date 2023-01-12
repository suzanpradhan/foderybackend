from json.decoder import JSONDecoder
import re
from django import http
from django.contrib.auth.models import User
from django.core.mail.message import EmailMultiAlternatives
from django.http import request
from django.contrib.auth import login
from urllib.parse import urlencode, quote_plus
from django.http.response import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponseNotFound,
    JsonResponse,
)
from django.views import generic
from django.views.generic import base
import firebase_admin

from firebase_admin import credentials

from firebase_admin import auth
from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView
import requests
from rest_framework.response import Response
from rest_framework import authentication, exceptions, permissions, serializers
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.parsers import JSONParser
from CustomUser.models import Profile, UserProfile
from CustomUser.orderplaced import get_order_placed_html, make_verification_email
from General.models import Review
from General.serilaizers import ReviewSerializer
from Order.models import Cart, Order
from Settings.models import Reward, User_Coupons
from fodery.decorator import check_token
from .utils import generate_access_token, generate_refresh_token
from CustomUser.serializer import (
    AddressSerializer,
    ProfileSer,
    ProfileSeriL,
    ProfileSerializer,
    UserSer,
    UserSerializer,
)
from django.core.mail import send_mail
from fodery import settings
import jwt
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, mixins, serializers
from .models import Address, Refer
import jwt
from jwt import exceptions as e
from django.utils.decorators import method_decorator
import datetime
import json
import secrets
import os
import binascii
from pyfacebook import GraphAPI
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError
from django.db.models.query_utils import Q


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = UserProfile.objects.filter(Q(email=data))
            print(associated_users)
        if associated_users.exists():
            for user in associated_users:
                subject = "Password Reset Requested"
                email_template_name = "password_reset_email.txt"
                c = {
                "email":user.email,
                'domain':'127.0.0.1:8000',
                'site_name': 'Website',
                "uid": base64.urlsafe_b64encode(force_bytes(user.pk)).decode(),
                "user": user,
                'token': default_token_generator.make_token(user),
                'protocol': 'http',
                }
                email = render_to_string(email_template_name, c)
                try:
                    send_mail(subject, email, settings.EMAIL_HOST_USER , [user.email], fail_silently=False)
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                return redirect("password_reset_done")
    else:
        password_reset_form = PasswordResetForm()
        return render(request=request, template_name="password_reset.html", context={"password_reset_form":password_reset_form})

def password_reset_confirm(request,uidb64, token):
    if request.method == "GET":
        if (uidb64) and (token):
            print(force_text(base64.urlsafe_b64decode(uidb64).decode()))
            user = UserProfile.objects.filter(id=force_text(base64.urlsafe_b64decode(uidb64).decode())).first()
            form = SetPasswordForm(user=user)
            return render(request=request, template_name="password_reset_confirm.html", context={"set_password_form":form})
    else:
        if (request.POST.get("new_password1") == request.POST.get("new_password2")):
            user = UserProfile.objects.filter(id=force_text(base64.urlsafe_b64decode(uidb64).decode())).first()
            user.set_password(request.POST.get("new_password1"))
            user.save()
        return redirect("password_reset_complete")
        

def decypher(token):
    data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    return data["user"]


def encrypt(payload):
    token = jwt.encode(payload, settings.SECRET_KEY)
    return token


def smtp(payload, email, base_url:str, username: str):       
    token = encrypt({"user": payload})
    subject = "Fodery - Email Verification"
    message = (
        "Hello, "
        + " Please click on this link to activate your account: "
        + f"{base_url}/user/activate/?token="
        + str(token)
    )
    html_context=make_verification_email(verification_link= (base_url +'/user/activate/?token='+str(token)), username= username)
    recepient = email
    print(base_url)
    msg=EmailMultiAlternatives(subject,message,settings.EMAIL_HOST_USER,[recepient])
    msg.attach_alternative(html_context,"text/html")
    msg.send()

@csrf_exempt
def smtpChangePw(payload, email):
    token = encrypt(
        {
            "user": payload,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15),
            "iat": datetime.datetime.utcnow(),
        }
    )
    subject = "Request to change Password."
    message = (
        "You have requested to change your password , "
        + " Please click on this link to do so: "
        + "http://127.0.0.1:8000/user/changePassword/"
        + str(token)
    )
    print(message)
    print(token)
    recepient = email

class ForgetPasswordBeta(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")

        if email is None: 
            raise exceptions.NotAcceptable("Email is required.")
        user = UserProfile.objects.filter(email=email).first()
        if user is None:
            raise exceptions.NotFound("User not found!")

        subject = "Password Reset Requested - c"
        email_template_name = "templates/password_reset_email.txt"
        c = {
        "email":user.email,
        'domain':request.get_host(),
        'site_name': 'smtp App',
        "uid": base64.urlsafe_b64encode(force_bytes(user.pk)).decode(),
        "user": user,
        'token': default_token_generator.make_token(user),
        'protocol': 'http',
        }
        email = render_to_string(email_template_name, c)
        try:
            send_mail(subject, email, settings.EMAIL_HOST_USER , [user.email], fail_silently=False)
        except BadHeaderError:
            return exceptions.NotFound('Invalid header found.')
        return Response(data=f"An email has been sent to {user.email}")
        
        # token = encrypt(
        #     {
        #         "user": user.id,
        #         "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15),
        #         "iat": datetime.datetime.utcnow(),
        #     }
        # )
        # subject = "Request to change Password."
        # message = (
        #     "You have requested to change your password , "
        #     + " Please click on this link to do so: "
        #     + "http://127.0.0.1:8000/user/changePassword/"
        #     + str(token)
        # )
        # print(message)
        # print(token)
        # return Response(data="success")



def token_validity(request):
    token = request.headers.get("token")
    try:
        data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        try:
            current_user=UserProfile.objects.get(id=data['user_id'])
            if current_user:
                return HttpResponse("Token is valid.")
            else:
                return HttpResponseNotFound('User not Found.')
        except ModuleNotFoundError:
            return HttpResponseForbidden('Authentication Error.')
    except e.ExpiredSignatureError:
        return HttpResponseBadRequest("Token Expired, Please refetch access token")
    except e.InvalidSignatureError:
        return HttpResponseForbidden("Token Invalid")
    except e.DecodeError:
        return HttpResponseForbidden("Token Invalid")


@csrf_exempt
def activation(request):
    try:
        token_get = request.GET.get("token")

        decrypt = decypher(bytes(token_get, "utf-8"))
        user = UserProfile.objects.get(id=decrypt)
        if user:
            user.is_active = True
            user.save()
    except:
        return HttpResponseBadRequest("Verification Failed.")
    return HttpResponse("Congrats, Your account is activaed.")


class Login(APIView):
    # queryset = UserSerializer.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")
        response = Response()

        if (email is None) or (password is None):
            raise exceptions.AuthenticationFailed("email and password required")

        user = UserProfile.objects.filter(email=email).first()
        if user is None:
            profile = Profile.objects.filter(phone=email).first()
            if profile is None:
                raise exceptions.AuthenticationFailed("user not found")
            else:
                user = profile.user
        if not user.check_password(password):
            raise exceptions.AuthenticationFailed("wrong password")

        serialized_user = UserSerializer(user).data
        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)

        response.set_cookie(key="refreshtoken", value=refresh_token, httponly=True)
        response.data = {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

        return response


class Register(APIView):

    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        email = data["email"]
        data["user"] = {
            "username": data["email"].split('@')[0],
            "email": data["email"],
            "password": data["password"],
        }
        print(data["user"])
        # try:
        #     refer=data['refer']
        # except:
        #     refer=None
        try:
            userp = UserProfile.objects.get(email=data["email"])
        except:
            userp = None
        try:
            prof = Profile.objects.get(email=data["email"])
        except:
            prof = None

        if userp != None or prof != None:
            raise exceptions.NotAcceptable("Username or Email already in use.") 

        serializer2 = ProfileSerializer(data=data)
        
        if serializer2.is_valid():
            serializer2.save()
            user = UserProfile.objects.get(email=email)
            
            cartInts = Cart()
            cartInts.user = user
            cartInts.save()
            print("kjhfgfxchgjhkgjhliuiyf")
            print(request.get_host() + "helajhljgasl")
            smtp(user.pk, email, base_url=request.get_host(), username=user.profile_full_name())

            # if refer:
            #     obj=Refer.objects.filter(id=refer).first()
            #     if not obj:
            #         raise exceptions.NotFound('Invalid Refer.')
            #     obj.referedTo=user
            #     obj.save()

            access_token = generate_access_token(user)
            refresh_token = generate_refresh_token(user)
            return Response({
                "status": "User succesfully created.",
                "access_token": access_token,
                "refresh_token": refresh_token,
            })
        else:
            print(serializer2.errors)
            raise exceptions.ValidationError("User validation Error")

@method_decorator(check_token, name="dispatch")
class referCheck(APIView):
    def post(self,request,*args, **kwargs):
        refer=request.data.get('refer')
        if refer:
            user=Profile.objects.filter(refer_code=refer).first()
            if not user:
                raise exceptions.NotFound('Invalid Code.')
            refer=Refer.objects.create(referedBy=user.user)
            return Response({'referId':refer.id})

@method_decorator(check_token, name="dispatch")
class ReferMe(APIView):
    def post(self, request,*args, **kwargs):
        data = JSONParser().parse(request)
        try:
            refer=data['refer_code']
        except:
            refer=None
        if refer:
            # try:
            user=Profile.objects.filter(refer_code=refer).first()
            if not user:
                raise exceptions.NotFound('Invalid Code.')
            referInst=Refer.objects.create(referedBy=user.user)
            referInst.referedTo=self.kwargs["user"]
            referInst.save()
            return Response({'referId':referInst.id, "referedBy": user.fname + user.lname})
        else:
            return HttpResponseBadRequest("Referral Code is requried.")

                

# class GoogleLogin(APIView):
#     def post(self, request, *args, **kwargs):
#         try:
#             token=request.POST.get("token")
#             # if token is None:
#             #     raise exceptions.bad_request("Token invalid.")
#             # decoded_token = auth.verify_id_token("token")
#             # uid = decoded_token['uid']
#             # provider = decoded_token['firebase']['sign_in_provider']
#             # image = None
#             # name = None
#             # if "name" in decoded_token:
#             #     name = decoded_token['name']
#             # if "picture" in decoded_token:
#             #     image = decoded_token['picture']
#             try:
#                 user = auth.get_user("vTJHIi9BV7MmyM51Lzirwo6Z2bJ3")
#                 email = user.email
#                 if user:
#                     print(email)
#                     user_obj,created=UserProfile.objects.get_or_create(email=email,is_active=True)
#                     socialAuth,created=SoicalID.objects.get_or_create(user=user_obj,google=token)
#                     access_token = generate_access_token(user_obj)
#                     refresh_token = generate_refresh_token(user_obj)
#                     response = Response()
#                     response.set_cookie(key="refreshtoken", value=refresh_token, httponly=True)
#                     response.data = {
#                         "access_token": access_token,
#                         "refresh_token": refresh_token,
#                     }

#                     return response
#                 else:
#                     return HttpResponseNotFound("User not found.")
#             except:
#                 return HttpResponseNotFound("User not found.")
#         except:
#             return HttpResponseBadRequest("Invalid Token.")


@method_decorator(check_token, name="dispatch")
class UpdateProfile(generics.UpdateAPIView):
    def post(self, request, *args, **kwargs):
        data=request.data
        print(data)
        instance = Profile.objects.filter(user=self.kwargs["user"]).first()
        if instance is None:
            raise exceptions.NotFound("Profile doesn't exist.")
        serializer = ProfileSer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response("Profile updated successfully.")

@method_decorator(check_token, name="dispatch")
class GetUserProfile(APIView):
    def get(self, request, *args, **kwargs):
        profile=Profile.objects.get(user=self.kwargs['user'])
        serializer=ProfileSerializer(profile,customizeFields=["id","avatar","fname","lname","coverImage","bio","gender"])

        return Response(serializer.data)



@method_decorator(check_token, name="dispatch")
class UpdateUserPw(APIView):
    def post(self, request, *args, **kwargs):
        currentPassword = request.data.get("currentPassword")
        newPw1 = request.data.get("newPassword")
        newPw2 = request.data.get("validatePassword")
        print("here")
        if newPw1 is not None:
            if newPw1 == newPw2:
                user_obj = UserProfile.objects.get(id=self.kwargs["user"].id)
                print(user_obj.email)
                print(newPw1)

                if user_obj.check_password(currentPassword):
                    user_obj.set_password(newPw1)
                    user_obj.save()
                    return HttpResponse("Password Changed Successfully.")
                else:
                    raise exceptions.ValidationError("Password Error, Please check again.")
            else:
                raise exceptions.NotAcceptable("New passwords didn't matched.")
        else:
            raise exceptions.NotAcceptable("Password is required.")

@method_decorator(check_token, name="dispatch")
class SetPw(APIView):
    def post(self, request, *args, **kwargs):
        newPw1 = request.data.get("newPassword")
        newPw2 = request.data.get("validatePassword")

        if newPw1 is None or newPw2 is None:
            raise exceptions.ValidationError("Password cannot be none")
        
        if newPw1 != newPw2:
            raise exceptions.ValidationError("Passwords don't match.")

        if len(newPw1)<8:
            raise exceptions.ValidationError("Minimum length must be 8.")

        
        user_obj = UserProfile.objects.get(id=self.kwargs["user"].id)

        user_obj.set_password(newPw1)
        return HttpResponse("Password Changed Successfully.")



@method_decorator(check_token, name="dispatch")
class ForgotPassword(APIView):
    def get(self, request, *args, **kwargs):
        user_obj = UserProfile.objects.get(id=self.kwargs["user"].id)
        smtpChangePw(self.kwargs["user"].id, user_obj.email)

    def post(self, request, token, *args, **kwargs):
        try:
            decrypt = decypher(bytes(token, "utf-8"))
            user_obj = UserProfile.objects.filter(id=decrypt).first()

            if user_obj is None:
                raise exceptions.AuthenticationFailed("User not found")

            user_obj.set_password(request.data.get("password"))
            user_obj.save()
            return HttpResponse("Success")

        except jwt.DecodeError:
            raise exceptions.AuthenticationFailed(
                {"message": "Refresh token error, please try again.", "statusCode": 106}
            )
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed(
                {
                    "message": "expired refresh token, please login again.",
                    "statusCode": 106,
                }
            )

@method_decorator(check_token, name="dispatch")
class AddressView(APIView):
    def post(self, request, *args, **kwargs):
        data=request.data
        data['state_id']=data.pop('state')
        data['city_id']=data.pop('city')
        data['country_id']=data.pop('country')
        data['user']=self.kwargs['user']


        if Address.objects.filter(label=data['label'], user=self.kwargs["user"]).exists():
            raise exceptions.NotAcceptable("Label already used.")
        
        Address.objects.create(**data)
        return HttpResponse("Success")


# class AddressView(generics.CreateAPIView):
#     serializer_class = AddressSerializer


@method_decorator(check_token, name="dispatch")
class AddressUpDelView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    lookup_field = "id"

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = generics.get_object_or_404(queryset, **filter_kwargs)
        
        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        if obj.user==self.kwargs['user']:
            return obj
        else:
            raise exceptions.NotAcceptable("User not valid.")

    def post(self, request, *args, **kwargs):

        return self.partial_update(request, *args, **kwargs)


# @method_decorator(check_token, name="dispatch")
# class AddressUpDelView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Address.objects.all()
#     serializer_class = AddressSerializer


# class AddressUpDelView(generics.RetrieveUpdateDestroyAPIView):
#     def post(self, request, *args, **kwargs):
#         return self.partial_update(request, *args, **kwargs)


@method_decorator(csrf_exempt, name="dispatch")
class DeliveryLogin(APIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")

        response = Response()

        if (email is None) or (password is None):
            raise exceptions.AuthenticationFailed("email and password required")

        group = UserProfile.objects.filter()
        user = UserProfile.objects.filter(email=email, groups__name="delivery").first()
        if user is None:
            raise exceptions.AuthenticationFailed("user not found")
        if not user.check_password(password):
            raise exceptions.AuthenticationFailed("wrong password")

        serialized_user = UserSerializer(user).data
        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)

        response.set_cookie(key="refreshtoken", value=refresh_token, httponly=True)
        response.data = {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

        return response


@method_decorator(check_token, name="dispatch")
class GetUser(APIView):
    def get(self, request, *args, **kwargs):
        response = Response()
        if Profile.objects.filter(user_id=self.kwargs["user"].id).exists():
            reward_obj = Reward.objects.filter(user=self.kwargs["user"])
            profile_obj = Profile.objects.filter(user_id=self.kwargs["user"].id).first()
            order_query = Order.objects.filter(user=self.kwargs["user"])
            coupon_query = User_Coupons.objects.filter(
                user=self.kwargs["user"], used=True
            )

            response.data = {
                "profile": ProfileSerializer(profile_obj).data,
                "user": UserSer(self.kwargs["user"]).data,
                "reward": reward_obj[0].points if reward_obj.exists() else 0,
                "orderCount": order_query.count() if order_query.exists() else 0,
                "coupons": coupon_query.count() if coupon_query.exists() else 0,
            }
            return response
        else:
            response.data = "User Profile Not Found."
            response.status_code = 701
            return response


@method_decorator(check_token, name="dispatch")
class GetUserAddress(generics.ListAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def get_queryset(self):
        queryset = Address.objects.filter(user_id=self.kwargs["user"].id)
        return queryset


import os
import random,string
import google_apis_oauth
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

from django.shortcuts import HttpResponseRedirect

# The url where the google oauth should redirect
# after a successful login.
REDIRECT_URI = 'https://fod.suzanpradhan.com.np/user/google/callback/'
# REDIRECT_URI = 'exp://192.168.1.73:19000'


# Authorization scopes required
SCOPES = ['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email', "openid"]

JSON_FILEPATH = os.path.join(os.getcwd(), 'client9.json')

def RedirectGoogleSignin(request):
    oauth_url = google_apis_oauth.get_authorization_url(
        JSON_FILEPATH, SCOPES, REDIRECT_URI)
    return HttpResponseRedirect(oauth_url)

def CallbackGoogleSignin(request):
    try:
        credentials = google_apis_oauth.get_crendentials_from_callback(
            request,
            JSON_FILEPATH,
            SCOPES,
            REDIRECT_URI
        )
        stringified_token = google_apis_oauth.stringify_credentials(
            credentials)
        stringified_token = json.loads(stringified_token)
        response = requests.get(f"https://www.googleapis.com/oauth2/v3/userinfo?access_token={stringified_token['token']}")
        jsonData = response.json()
        print(jsonData)
        # all = string.ascii_letters + string.digits + string.punctuation
        # password = "".join(random.sample(all,12))
        if jsonData['email']:
            profileData = {
                "fname":jsonData['given_name'],
                "lname":jsonData['family_name'],
                "image_url": jsonData["picture"]
            }
            user, userExist = UserProfile.objects.get_or_create(email=jsonData["email"], username=str(jsonData["email"]).split("@")[0])
            user.save()
            profile, _ = Profile.objects.get_or_create(user=user)
            profile.__dict__.update(profileData)
            profile.save()
            # if not userExist:
            cartInts, isExist = Cart.objects.get_or_create(user=user)
            if isExist:
                cartInts.user = user
            cartInts.save()
            user.backend = settings.AUTH_PASSWORD_VALIDATORS[0]['NAME']
            login(request, user)
            access_token = generate_access_token(user)
            refresh_token = generate_refresh_token(user)
            HttpResponseRedirect.allowed_schemes.append('foodery')
            print(f"foodery://?access_token={access_token}&refresh_token={refresh_token}")
            # return HttpResponseRedirect(f"foodery://?access_token={access_token}&refresh_token={refresh_token}")
            return HttpResponseRedirect(f"foodery://?access_token={access_token}&refresh_token={refresh_token}")

        return HttpResponseBadRequest("Login Failed")
    except google_apis_oauth.InvalidLoginException:
        return HttpResponseBadRequest("Login Failed")

def RedirectFacebookSignin(request):
    url = "https://graph.facebook.com/oauth/authorize"
    params = {
        'client_id': settings.FB_APP_ID,
        'redirect_uri': "https://localhost:8000/user/facebook/callback/",
        'scope': 'email,public_profile,user_birthday'
    }
    url += '?' + urlencode(params, quote_via=quote_plus)
    return HttpResponseRedirect(url)
    # oauth_url = google_apis_oauth.get_authorization_url(
    #     JSON_FILEPATH, SCOPES, REDIRECT_URI)
    # return HttpResponseRedirect(oauth_url)

def CallbackFacebookSignin(request):
    code = request.GET.get('code')
    print(code)
    url = 'https://graph.facebook.com/v2.10/oauth/access_token'
    params = {
        'client_id': settings.FB_APP_ID,
        'client_secret': settings.FB_APP_SECRET,
        'code': code,
        'redirect_uri': "https://www.google.com",
    }
    response = requests.get(url, params=params)
    print(response.content)
    params = response.json()
    return HttpResponse(params)
    params.update({
        'fields': 'id,last_name,first_name,picture,birthday,email,gender'
    })
    url = 'https://graph.facebook.com/me'
    user_data = requests.get(url, params=params).json()
    email = user_data.get('email')
    fname = user_data.get('first_name')
    lname = user_data.get('last_name')
    picture = user_data.get('picture')
    # if email:
    #     user, _ = User.objects.get_or_create(email=email, username=email)
    #     gender = user_data.get('gender', '').lower()
    #     dob = user_data.get('birthday')
    #     if gender == 'male':
    #         gender = 'M'
    #     elif gender == 'female':
    #         gender = 'F'
    #     else:
    #         gender = 'O'
    #     data = {
    #         'first_name': user_data.get('first_name'),
    #         'last_name': user_data.get('last_name'),
    #         'fb_avatar': user_data.get('picture', {}).get('data', {}).get('url'),
    #         'gender': gender,
    #         'dob': datetime.strptime(dob, "%m/%d/%Y") if dob else None,
    #         'is_active': True
    #     }
    #     user.__dict__.update(data)
    #     user.save()
    #     user.backend = settings.AUTHENTICATION_BACKENDS[0]
    #     login(request, user)
    # else:
    #     messages.error(
    #         request,
    #         'Unable to login with Facebook Please try again'
    #     )
    return HttpResponse(user_data)

@method_decorator(check_token, name="dispatch")
class CheckPhoneVerification(APIView):
    def get(self, request, *args, **kwargs):
        user = self.kwargs["user"]
        response = Response()
        if user.profile_exists():
            if user.profile().isPhoneVerified and user.profile().phone:
                response.data = {
                    "status": True
                }
            else:
                response.status_code = 901
                response.data = "Phone not verified."
        else:
            response.status_code = 901
            response.data = "Phone not verified."   
        return response

import pyotp
import base64
@method_decorator(check_token, name="dispatch")
class VerifyUserPhone(APIView):
    def post(self, request, *args, **kwargs):
        try:
            user = self.kwargs["user"]
            response = Response()
            if request.data.get("phone"):
                phone = request.data.get("phone")
                if user.profile().isPhoneVerified and user.profile().phone == phone:
                    response.status_code = 400
                    response.data = {
                        "status": False,
                        "message": "Your phone is already verified."
                    }
                    return response

                if Profile.objects.filter(phone=phone).exists():
                    response.status_code = 400
                    response.data = {
                        "status": False,
                        "message": "Phone number is aleady registered."
                    }
                    return response
                userProfile = user.profile()
                if userProfile.update_at_rt == None:
                    userProfile.update_at_rt = datetime.datetime.now(tz=timezone.utc)
                if (int((datetime.datetime.now(tz=timezone.utc) - datetime.timedelta(hours=1)).timestamp()) < int(userProfile.update_at_rt.timestamp())):
                    if (userProfile.requestTimes - userProfile.lastRequestTimes) > 5:
                        response.status_code = 902
                        response.data = {
                                "status": False,
                                "message": "You have been blocked from requesting more phone verification. Please try again after an hour."
                            }
                        return response
                else:
                    userProfile.lastRequestTimes = userProfile.requestTimes
                    userProfile.update_at_rt = datetime.datetime.now(tz=timezone.utc)
                requestTimes = userProfile.requestTimes + 1
                userProfile.requestTimes = requestTimes
                userProfile.save()
                totp = pyotp.TOTP(base64.b32encode((settings.OTP_SECRET_KEY + str(phone) + str(requestTimes)).encode('utf-8')), interval=300)
                token = totp.now()
                print(token)
                url = settings.AAKASH_SMS_API_BASE_URL
                params = {
                    'auth_token': settings.AAKASH_SMS_TOKEN,
                    'to': phone,
                    'text': f"Your Fodery OTP code is {token}"
                }
                url += '?' + urlencode(params, quote_via=quote_plus)
                print(url)
                dataResponse = requests.get(url)
                jsonData = dataResponse.json()
                if (jsonData['error']):
                    response.status_code = 400
                    response.data = {
                        "status": False,
                        "message": "Can't send OTP code."
                    }
                else:
                    response.data = {
                        "status": True,
                        "message": f"Your OTP code has been sent to {phone}."
                    }
            else:
                response.status_code = 400
                response.data = {
                    "status": False,
                    "message": "Phone Number is required."
                }
            return response
        except:
            return HttpResponseBadRequest("Server Error.")

import pyotp
import base64
import datetime
from django.utils import timezone
@method_decorator(check_token, name="dispatch")
class TestVerifyUserPhone(APIView):
    def post(self, request, *args, **kwargs):
        # try:
            user = self.kwargs["user"]
            response = Response()
            if request.data.get("phone"):
                phone = request.data.get("phone")
                if user.profile().isPhoneVerified and user.profile().phone == phone:
                    response.status_code = 400
                    response.data = {
                        "status": False,
                        "message": "Phone Number is already verified."
                    }
                    return response
                userProfile = user.profile()
                if userProfile.update_at_rt == None:
                    userProfile.update_at_rt = datetime.datetime.now(tz=timezone.utc)
                if (int((datetime.datetime.now(tz=timezone.utc) - datetime.timedelta(hours=1)).timestamp()) < int(userProfile.update_at_rt.timestamp())):
                    if (userProfile.requestTimes - userProfile.lastRequestTimes) > 5:
                        response.status_code = 902
                        response.data = {
                                "status": False,
                                "message": "You have been blocked from requesting more phone verification. Please try again after an hour."
                            }
                        return response
                else:
                    userProfile.lastRequestTimes = userProfile.requestTimes
                    userProfile.update_at_rt = datetime.datetime.now(tz=timezone.utc)
                requestTimes = userProfile.requestTimes + 1
                userProfile.requestTimes = requestTimes
                userProfile.save()
                totp = pyotp.TOTP(base64.b32encode((settings.OTP_SECRET_KEY + str(phone) + str(requestTimes)).encode('utf-8')), interval=300)
                token = totp.now()
                print(token)
                url = settings.AAKASH_SMS_API_BASE_URL
                params = {
                    'auth_token': settings.AAKASH_SMS_API_BASE_URL,
                    'to': phone,
                    'text': f"Your Fodery OTP code is {token}"
                }
                url += '?' + urlencode(params, quote_via=quote_plus)
                # dataResponse = requests.get(url)
                # jsonData = dataResponse.json()
                # if (jsonData['error']):
                #     response.status_code = 400
                #     response.data = {
                #         "status": False,
                #         "message": "Can't send OTP code."
                #     }
                # else:
                    
                response.data = {
                    "code":token,
                    "status": True,
                    "message": f"Your OTP code has been sent to {phone}."
                }
            else:
                response.status_code = 400
                response.data = {
                    "status": False,
                    "message": "Phone Number is required."
                }
            print(response.data)
            return response
        # except:
        #     return HttpResponseBadRequest("Server Error.")

@method_decorator(check_token, name="dispatch")
class VerifyOTPCode(APIView):
    def post(self, request, *args, **kwargs):
        user = self.kwargs["user"]
        response = Response()
        if request.data.get("code") and request.data.get("code"):
            phone = request.data.get("phone")
            code = request.data.get("code")
            userProfile = user.profile()
            requestTimes = userProfile.requestTimes
            totp = pyotp.TOTP(base64.b32encode((settings.OTP_SECRET_KEY + str(phone) + str(requestTimes)).encode('utf-8')), interval=300)
            if (totp.verify(code)):
                userProfile.phone = phone
                userProfile.isPhoneVerified = True
                # userProfile.requestTimes = userProfile.requestTimes + 1
                userProfile.save()
                response.data = {
                    "status": True,
                    "message": "Your phone is now verified."
                }
            else:
                response.status_code = 400
                response.data = {
                    "status": False,
                    "message": "Your OTP code is incorrect."
                }
        else:
            response.status_code = 400
            response.data = {
                "status": False,
                "message": "OTP code and Phone Number is required."
            }
        return response

@method_decorator(check_token, name="dispatch")
class PasswordEmpty(APIView):
    def get(self,request,*args, **kwargs):
        user=self.kwargs['user']
        if user.password:
            return Response({"status":False})
        else:
            return Response({"status":True})


class ChangeDefault(generics.UpdateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    lookup_field = "id"
    def post(self, request, *args, **kwargs):
        query=Address.objects.filter(user=self.kwargs['user'],isDefault=True)
        for _ in query:
            _.isDefault=False
            _.save()
        return self.partial_update(request, *args, **kwargs)


# DEACTIVE ACCOUNT
@method_decorator(check_token, name="dispatch")
class DeactivateAccount(APIView):
    def get(self, request, *args, **kwargs):
        user = self.kwargs['user']
        if not user.is_active:
            raise exceptions.NotAcceptable("Account is already deactive.")
        else:
            user.is_active = False
            user.save()
            return Response({"status": True, "message": "Account has been deactivated."})


@method_decorator(check_token, name="dispatch")
class ReviewHistory(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        queryset = Review.objects.filter(user_id=self.kwargs["user"].id)
        return queryset
