import datetime
from django.http.response import HttpResponse
import jwt
from django.conf import settings
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from rest_framework import exceptions
from CustomUser.models import UserProfile
from rest_framework.response import Response
from CustomUser.serializer import UserSerializer
from rest_framework.decorators import api_view

def generate_access_token(user):

    access_token_payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=5),
        'iat': datetime.datetime.utcnow(),
    }
    access_token = jwt.encode(access_token_payload,
                              settings.SECRET_KEY, algorithm='HS256')
    return access_token


def generate_refresh_token(user):
    refresh_token_payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
        'iat': datetime.datetime.utcnow()
    }
    refresh_token = jwt.encode(
        refresh_token_payload, settings.SECRET_KEY, algorithm='HS256')

    return refresh_token

@api_view(['POST'])
@csrf_exempt
def refresh_token_view(request):
    
    refresh_token = request.data.get('refresh_token')
    if refresh_token is None:
        raise exceptions.AuthenticationFailed(
            'Authentication credentials were not provided.')
    try:
        payload = jwt.decode(
            refresh_token, settings.SECRET_KEY, algorithms=['HS256'])
    except jwt.DecodeError:
        raise exceptions.AuthenticationFailed(
            {"message":'Refresh token error, please try again.', 
            })
    except jwt.ExpiredSignatureError:
        return HttpResponse(
            'expired refresh token, please login again.', status=406
            
            )

    user = UserProfile.objects.filter(id=payload.get('user_id')).first()
    if user is None:
        raise exceptions.AuthenticationFailed('User not found')

    if not user.is_active:
        raise exceptions.AuthenticationFailed('user is inactive')


    access_token = generate_access_token(user)
    return Response({'access_token': access_token})
