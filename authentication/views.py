
from urllib.parse import urlencode
from rest_framework import serializers
from rest_framework.views import APIView
from django.conf import settings
from django.shortcuts import redirect
from rest_framework.response import Response
from .mixins import PublicApiMixin, ApiErrorsMixin
from .utils import (
    google_get_access_token, 
    google_get_user_info, 
    generate_tokens_for_user, 
    google_refresh_access_token, 
    google_validate_admin,
    google_get_user_list
    )
from .models import User, GoogleAccessTokens
from rest_framework import status
from .serializers import UserSerializer
from icecream import ic
from rest_framework_simplejwt.tokens import AccessToken

class GoogleLoginApi(PublicApiMixin, ApiErrorsMixin, APIView):
    class InputSerializer(serializers.Serializer):
        code = serializers.CharField(required=False)
        error = serializers.CharField(required=False)

    def get(self, request, *args, **kwargs):
        # ic(request)
        input_serializer = self.InputSerializer(data=request.GET)
        input_serializer.is_valid(raise_exception=True)
        validated_data = input_serializer.validated_data
        code = validated_data.get('code')
        error = validated_data.get('error')

        login_url = f'{settings.BASE_FRONTEND_URL}'
        
        if error or not code:
            params = urlencode({'error': error})
            return redirect(f'{login_url}?{params}')

        redirect_uri = f'{settings.BASE_FRONTEND_URL}/google'
        # ic(code)
        response_info = google_get_access_token(code=code, 
                                               redirect_uri=redirect_uri)

                                               
        # check if access_token exists
        if not response_info.get('access_token'):
            return Response({'error': 'access_token could not be obrained not found'}, status=status.HTTP_400_BAD_REQUEST)

        access_token = response_info['access_token']
        refresh_token = response_info['refresh_token']
    
        user_data = google_get_user_info(access_token=access_token)
        ic(user_data)

        try:
            user = User.objects.get(email=user_data['email'])
            googleAccessTokens = GoogleAccessTokens.objects.get(user=user)
            googleAccessTokens.access_token = access_token
            googleAccessTokens.refresh_token = refresh_token
            googleAccessTokens.save()
            
            access_token, refresh_token = generate_tokens_for_user(user)
            response_data = {
                'user': UserSerializer(user).data,
                'access_token': str(access_token),
                'refresh_token': str(refresh_token)
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            # username = user_data['email'].split('@')[0]
            first_name = user_data.get('given_name', '')
            last_name = user_data.get('family_name', '')
            picture = user_data.get('picture', '')

            user = User.objects.create(
                email=user_data['email'],
                picture=picture,
                first_name=first_name,
                last_name=last_name,
                registration_method='google'
            )
            
            googleAccessTokens = GoogleAccessTokens.objects.create(
                user = user,
                access_token=access_token,
                refresh_token=refresh_token
                )
            googleAccessTokens.save()
            
            access_token, refresh_token = generate_tokens_for_user(user)
            response_data = {
                'user': UserSerializer(user).data,
                'access_token': str(access_token),
                'refresh_token': str(refresh_token)
            }
            return Response(response_data, status=status.HTTP_200_OK)


class GoogleUserListApi(PublicApiMixin, ApiErrorsMixin, APIView):
    
    def get(self, request, *args, **kwargs):
        bearer = request.META.get('HTTP_AUTHORIZATION')
        token = bearer.split(' ')[1]
        user_id = AccessToken(token)["user_id"]
        user = User.objects.get(id=str(user_id))
        
        googleAccessTokens = GoogleAccessTokens.objects.get(user=user)
        refresh_token = googleAccessTokens.refresh_token
        google_access_response = google_refresh_access_token(refresh_token=refresh_token)
        access_token = google_access_response['access_token']
        
        if google_validate_admin(access_token=access_token, user_email=user.email):
            user_list = google_get_user_list(access_token=access_token)
            ic(user_list)
            return Response(user_list, status=status.HTTP_200_OK)
        
            
        context = {
            "message": "User is not admin!"
        }
    
        return Response(context, status=status.HTTP_400_BAD_REQUEST)
