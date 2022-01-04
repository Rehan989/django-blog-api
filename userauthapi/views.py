from django.shortcuts import render
from rest_framework.response import Response
import requests
from djoser.conf import django_settings
from rest_framework.views import APIView
from rest_framework import permissions
from djoser import email
from rest_framework.decorators import (
    permission_classes,
)
# Create your views here.

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client

@permission_classes([permissions.AllowAny])
class UserActivationView(APIView):
    def post(self, request, uid, token):
        try:
            payload = {'uid': uid, 'token': token}
            protocol = 'https://' if request.is_secure() else 'http://'
            web_url = protocol +request.get_host()

            url= web_url+'/user/users/activation/'
            response = requests.post(url, data = payload)

            if response.status_code == 204:
                return Response({'success': 'User activated Successfully'})
            else:
                return Response(response.json())
        except Exception as e:
            return Response({'error':'Internal server error!'})
    def get(self, request, uid, token):
        return Response({'error':'Page not found!'})

@permission_classes([permissions.AllowAny])
class UserResetPassword(APIView):
    def post(self, request, uid, token):
        try:
            data = request.data
            # print(data)
            newPassword = data['newPassword']
            confirmNewPassword = data['confirmNewPassword']
            protocol = 'https://' if request.is_secure() else 'http://'
            web_url = protocol +request.get_host()

            payload = {'uid': uid, 'token': token, 'new_password':newPassword, 're_new_password':confirmNewPassword}
            url= web_url+'/user/users/reset_password_confirm/'
            response = requests.post(url, data = payload)

            if response.status_code == 204:
                return Response({'success': 'Password reset successful'})
            else:
                return Response(response.json())
        except KeyError:
            return Response({"error":'Not Allowed!'})
        except Exception as e:
            print(e)
            return Response({"error":"Internal server error!"})
    def get(self, request, uid, token):
        return Response({'error':'Page not found!'})


@permission_classes([permissions.AllowAny])
class UserResetUsername(APIView):
    def post(self, request, uid, token):
        try:
            data = request.data
            # print(data)
            newUsername = data['newUsername']
            protocol = 'https://' if request.is_secure() else 'http://'
            web_url = protocol +request.get_host()

            payload = {'uid': uid, 'token': token, 'new_username':newUsername}
            url= web_url+'/user/users/reset_username_confirm/'
            response = requests.post(url, data = payload)

            if response.status_code == 204:
                return Response({'success': 'Username reset successful'})
            else:
                return Response(response.json())
        except KeyError:
            return Response({"error":'Not Allowed!'})
        except Exception as e:
            print(e)
            return Response({"error":"Internal server error!"})
    def get(self, request, uid, token):
        return Response({'error':'Page not found!'})


# Overriding activation email
class ActivationEmail(email.ActivationEmail):
    template_name = 'email/activation.html'


class GoogleSignup(SocialLoginView):
    authentication_classes = [] # disable authentication
    adapter_class = GoogleOAuth2Adapter
    callback_url = "https://blog.prodev.pro"
    client_class = OAuth2Client