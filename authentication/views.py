
from urllib.parse import urlencode
from rest_framework import serializers
from rest_framework.views import APIView
from django.conf import settings
from django.shortcuts import redirect
from rest_framework.response import Response
from authentication.mixins import PublicApiMixin, ApiErrorsMixin
from authentication.utils import (
    google_get_access_token, 
    google_get_user_info, 
    generate_tokens_for_user, 
    google_refresh_access_token, 
    google_validate_admin,
    google_get_user_list,
    get_user_id_from_request
    )
from authentication.models import User, GoogleAccessTokens
from rest_framework import status
from authentication.serializers import UserSerializer
from icecream import ic
from organization.models import Company

class GoogleLoginApi(PublicApiMixin, ApiErrorsMixin, APIView):
    class InputSerializer(serializers.Serializer):
        code = serializers.CharField(required=False)
        error = serializers.CharField(required=False)

    def post(self, request, *args, **kwargs):
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
        # ic(user_data)

        try:
            user = User.objects.get(email=user_data['email'])
            googleAccessTokens = GoogleAccessTokens.objects.get(user=user)
            googleAccessTokens.access_token = access_token
            googleAccessTokens.refresh_token = refresh_token
            googleAccessTokens.save()
            
            access_token, refresh_token = generate_tokens_for_user(user)
            response_data = {
                # 'user': UserSerializer(user).data,
                'access': str(access_token),
                'refresh': str(refresh_token)
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
                # 'user': UserSerializer(user).data,
                'access': str(access_token),
                'refresh': str(refresh_token)
            }
            return Response(response_data, status=status.HTTP_200_OK)

class RegularLoginApi(PublicApiMixin, ApiErrorsMixin, APIView):
    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField()
        password = serializers.CharField()

    def post(self, request, *args, **kwargs):
        print("post request for login")
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        validated_data = input_serializer.validated_data
        email = validated_data.get('email')
        password = validated_data.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        if not user.check_password(password):
            return Response({'error': 'Invalid password'}, status=status.HTTP_404_NOT_FOUND)

        access_token, refresh_token = generate_tokens_for_user(user)
        response_data = {
            # 'user': UserSerializer(user).data,
            'access': str(access_token),
            'refresh': str(refresh_token)
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
    
class UserProfileApi(PublicApiMixin, ApiErrorsMixin, APIView):
    def get(self, request, *args, **kwargs):
        user_id = get_user_id_from_request(request)
        if not user_id:
            return Response({'error': 'user could not be identified by the token'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(id=user_id)
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
    

# ! apis for updating first name, last name, username, picture, password
class SetFirstNameApi(PublicApiMixin, ApiErrorsMixin, APIView):
    class InputSerializer(serializers.Serializer):
        first_name = serializers.CharField()

    def post(self, request, *args, **kwargs):
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        validated_data = input_serializer.validated_data
        first_name = validated_data.get('first_name')

        user_id = get_user_id_from_request(request)
        if not user_id:
            return Response({'error': 'user could not be identified by the token'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(id=user_id)
        user.first_name = first_name
        user.save()
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)

class SetLastNameApi(PublicApiMixin, ApiErrorsMixin, APIView):
    class InputSerializer(serializers.Serializer):
        last_name = serializers.CharField()

    def post(self, request, *args, **kwargs):
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        validated_data = input_serializer.validated_data
        last_name = validated_data.get('last_name')

        user_id = get_user_id_from_request(request)
        if not user_id:
            return Response({'error': 'user could not be identified by the token'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(id=user_id)
        user.last_name = last_name
        user.save()
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
    
class SetUsernameApi(PublicApiMixin, ApiErrorsMixin, APIView):
    class InputSerializer(serializers.Serializer):
        username = serializers.CharField()

    def post(self, request, *args, **kwargs):
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        validated_data = input_serializer.validated_data
        username = validated_data.get('username')

        user_id = get_user_id_from_request(request)
        if not user_id:
            return Response({'error': 'user could not be identified by the token'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(id=user_id)
        user.username = username
        user.save()
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
    
class SetUserPhotoApi(PublicApiMixin, ApiErrorsMixin, APIView):
    class InputSerializer(serializers.Serializer):
        picture = serializers.CharField()

        
    def post(self, request, *args, **kwargs):
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        validated_data = input_serializer.validated_data
        picture = validated_data.get('picture')

        user_id = get_user_id_from_request(request)
        if not user_id:
            return Response({'error': 'user could not be identified by the token'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(id=user_id)
        user.picture = picture
        user.save()
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
    
    
class SetUserPhoneApi(PublicApiMixin, ApiErrorsMixin, APIView):
    class InputSerializer(serializers.Serializer):
        phone = serializers.CharField()

        
    def post(self, request, *args, **kwargs):
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        validated_data = input_serializer.validated_data
        phone = validated_data.get('phone')

        user_id = get_user_id_from_request(request)
        if not user_id:
            return Response({'error': 'user could not be identified by the token'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(id=user_id)
        user.phone = phone
        user.save()
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
    
class setUserPasswordApi(PublicApiMixin, ApiErrorsMixin, APIView):
    class InputSerializer(serializers.Serializer):
        password = serializers.CharField()
        new_password = serializers.CharField()

        
    def post(self, request, *args, **kwargs):
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        validated_data = input_serializer.validated_data
        password = validated_data.get('password')
        new_password = validated_data.get('new_password')

        user_id = get_user_id_from_request(request)
        if not user_id:
            return Response({'error': 'user could not be identified by the token'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(id=user_id)
        if not user.check_password(password):
            return Response({'error': 'Invalid password'}, status=status.HTTP_404_NOT_FOUND)
        
        user.set_password(new_password)
        user.save()
        return Response({"status": "Password changed succesfuly"}, status=status.HTTP_200_OK)