from rest_framework import serializers
from .models import *

class SocialGoogleAuth(serializers.ModelSerializer):
    class Meta:
        model = GoogleUser
        fields = '__all__'