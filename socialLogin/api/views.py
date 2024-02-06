from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from socialLogin.serializer import SocialGoogleAuth


@api_view(['POST'])
def google_auth(request):
    """returns a view for google authentication"""
    # serializer = SocialGoogleAuth(data=request.data)
    print(request.data)

    return Response(request.data, status=200)


@api_view(['GET'])
def get_routes(request):
    """returns a view containing all the possible routes"""
    routes = [
        '/google',
    ]

    return Response(routes)
