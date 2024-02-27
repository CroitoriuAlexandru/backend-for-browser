from rest_framework import serializers
from authentication.models import User

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['username', "phone", 'picture', 'first_name', 'last_name', 'email']

