
from rest_framework import serializers
from homePage.models import HomeBackground, HomeLayout


 
class HomeBackgroundSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeBackground
        fields = '__all__'