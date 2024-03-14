from rest_framework import serializers
from authentication.models import User

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = [
            'id', 
            'username', 
            "phone", 
            'picture', 
            'first_name', 
            'last_name', 
            'email'
            ]

class InputSerializer(serializers.Serializer):
    char_input = serializers.CharField()


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=7, max_length=100)
    new_password = serializers.CharField(min_length=7, max_length=100)


