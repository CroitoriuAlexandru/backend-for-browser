from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from rest_framework_simplejwt.views import TokenObtainPairView

from organization.models import Company
from organization.serializer import CompanySerializer


# @permission_classes([IsAuthenticated])
@api_view(['POST'])
def set_organization(request):
    print(request)
    # user = request.user
    company_data = Company.objects.first()
    serializer = CompanySerializer(company_data, many=False)
    return Response(serializer.data)
    




@api_view(['GET'])
def get_routes(request):
    """returns a view containing all the possible routes"""
    routes = [
        '/api/organization/set_organization',
    ]

    return Response(routes)

# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)

#         token['username'] = user.username

#         return token

# class MyTokenObtainPairView(TokenObtainPairView):
#     serializer_class = MyTokenObtainPairSerializer

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_profile(request):
#     user = request.user
#     profile = user.profile
#     serializer = ProfileSerializer(profile, many=False)
#     return Response(serializer.data)
