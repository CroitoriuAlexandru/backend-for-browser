from django.shortcuts import render
from authentication.mixins import PublicApiMixin, ApiErrorsMixin
from rest_framework.views import APIView
from homePage.models import HomeBackground, MostUsedSites
from rest_framework.response import Response
from rest_framework import status
from homePage.serializers import HomeBackgroundSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from authentication.utils import get_user_id_from_request
from authentication.models import User
import icecream as ic  # Import the icecream module for logging
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework import serializers
from rest_framework import status

# Create your views here.
class add_background_image(PublicApiMixin, ApiErrorsMixin, APIView):
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(
        request_body=HomeBackgroundSerializer,
        responses={200: HomeBackgroundSerializer}
    )
    
    def post(self, request):
        user_id = get_user_id_from_request(request)
        image_data = request.data.get('image')
        homeBackground = HomeBackground.objects.create(user_id=user_id, image=image_data)
        homeBackground.save()
        self.serializer = HomeBackgroundSerializer(homeBackground)
        homeBackgrounds = HomeBackground.objects.filter(user_id=user_id)
        serializer = HomeBackgroundSerializer(homeBackgrounds, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class get_background_images(PublicApiMixin, ApiErrorsMixin, APIView):
    def get(self, request):
        user_id = get_user_id_from_request(request)
        homeBackgrounds = HomeBackground.objects.filter(user_id=user_id)
        serializer = HomeBackgroundSerializer(homeBackgrounds, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class remove_background_image(PublicApiMixin, ApiErrorsMixin, APIView):
    def post(self, request):
        print(request.data)
        print(request.data.get('image_id'))
        homeBackgroundId = request.data.get('image_id')
        homeBackground = HomeBackground.objects.get(id=homeBackgroundId)
        homeBackground.delete()
        homeBackgrounds = HomeBackground.objects.filter(user_id=homeBackground.user_id)
        serializer = HomeBackgroundSerializer(homeBackgrounds, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class save_most_used_sites(PublicApiMixin, ApiErrorsMixin, APIView):
    def post(self, request):
        user_id = get_user_id_from_request(request)
        print(request.data)
        # print(request.data.get('url'))

        return Response({"message": "all good"}, status=status.HTTP_200_OK)