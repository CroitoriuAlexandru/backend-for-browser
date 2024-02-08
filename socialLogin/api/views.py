from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from socialLogin.serializer import SocialGoogleAuth

from icecream import ic

@api_view(['POST'])
def google_auth(request):
    """returns a view for google authentication"""
    # serializer = SocialGoogleAuth(data=request.data)
    ic(request)
    ic(request.data)

    data={
        'google_user_id': request.data['id'],
        'email': request.data['email'],
        'verified_email': request.data['verified_email'],
        'picture': request.data['picture'],
        'family_name': request.data['family_name'],
        'given_name': request.data['given_name']
    }
    ic(data)
    
    serializer = SocialGoogleAuth(data=data)
    if serializer.is_valid():
        ic(serializer)
        serializer.save()
    else:
        ic(serializer.errors)



    # test = request.data['id']
    # serializer = request.data['id']
    # serializer['email'] = request.data['email']
    # serializer['verified_email'] = request.data['verified_email']
    # serializer['photo_url'] = request.data['photo_url']
    # serializer['family_name'] = request.data['family_name']
    # serializer['given_name'] = request.data['given_name']
    
    # ic(serializer)
    
    return Response(request.data, status=200)


@api_view(['GET'])
def get_routes(request):
    """returns a view containing all the possible routes"""
    routes = [
        '/google',
    ]

    return Response(routes)
