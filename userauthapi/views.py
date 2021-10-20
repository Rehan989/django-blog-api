from django.shortcuts import render
from rest_framework.response import Response
import requests
from djoser.conf import django_settings
from rest_framework.views import APIView
from rest_framework import permissions
from django.urls import reverse
from rest_framework.decorators import (
    api_view,
    permission_classes,
)
# Create your views here.


@permission_classes([permissions.AllowAny])
class UserActivationView(APIView):
    def get (self, request, uid, token):
        payload = {'uid': uid, 'token': token}
        protocol = 'https://' if request.is_secure() else 'http://'
        web_url = protocol +request.get_host()

        url= web_url+'/user/users/activation/'
        response = requests.post(url, data = payload)

        if response.status_code == 204:
            return Response({'success': 'User activated Successfully'})
        else:
            return Response(response.json())