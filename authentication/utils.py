
import requests
from typing import Dict, Any
from django.conf import settings
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from icecream import ic
from rest_framework_simplejwt.tokens import AccessToken
from organization.serializers import EmployeeSerializer
from authentication.models import User, GoogleAccessTokens
from organization.models import Company

GOOGLE_ID_TOKEN_INFO_URL = 'https://www.googleapis.com/oauth2/v3/tokeninfo'
GOOGLE_ACCESS_TOKEN_OBTAIN_URL = 'https://oauth2.googleapis.com/token'
# GOOGLE_ACCESS_TOKEN_OBTAIN_URL = 'https://oauth2.googleapis.com/token'
# GOOGLE_USER_INFO_URL = 'https://www.googleapis.com/oauth2/v3/userinfo'
GOOGLE_USER_INFO_URL = 'https://www.googleapis.com/oauth2/v1/userinfo'
GOOGLE_ADMIN_USER_LIST_USERS = "https://admin.googleapis.com/admin/directory/v1/users"

def generate_tokens_for_user(user):
    """
    Generate access and refresh tokens for the given user
    """
    serializer = TokenObtainPairSerializer()
    token_data = serializer.get_token(user)
    access_token = token_data.access_token
    refresh_token = token_data
    return access_token, refresh_token


def google_get_access_token(*, code: str, redirect_uri: str) -> str:
    data = {
        'code': code,
        'client_id': settings.GOOGLE_OAUTH2_CLIENT_ID,
        'client_secret': settings.GOOGLE_OAUTH2_CLIENT_SECRET,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code'
    }

    response = requests.post(GOOGLE_ACCESS_TOKEN_OBTAIN_URL, data=data)

    if not response.ok:
        raise ValidationError('Failed to obtain access token from Google.')

    return response.json()

def google_refresh_access_token(*, refresh_token: str) -> str:
    data = {
        'client_id': settings.GOOGLE_OAUTH2_CLIENT_ID,
        'client_secret': settings.GOOGLE_OAUTH2_CLIENT_SECRET,
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token'
    }

    response = requests.post(GOOGLE_ACCESS_TOKEN_OBTAIN_URL, data=data)

    if not response.ok:
        raise ValidationError('Failed to obtain access token from Google.')

    return response.json()

def google_get_user_info(*, access_token:  str) -> Dict[str, Any]:
    request = requests.Request('GET', GOOGLE_USER_INFO_URL, params={'access_token': access_token})
    prepared_request = request.prepare()
    response = requests.Session().send(prepared_request)

    # request_users = requests.Request('GET', GOOGLE_ADMIN_USER_LIST_USERS, params={'access_token': access_token})
    # prepared_request_users = request_users.prepare()
    # response_users = requests.Session().send(prepared_request_users)

    if not response.ok:
        raise ValidationError('Failed to obtain user info from Google.')

    return response.json()


def google_get_user_list(admin_id: str) -> [dict]:
    admin_user = User.objects.get(id=admin_id)
    google_token = GoogleAccessTokens.objects.get(user=admin_user)
    new_google_token = google_refresh_access_token(refresh_token=google_token.refresh_token)
    access_token = new_google_token["access_token"]
    domain = admin_user.email[admin_user.email.index('@')+1:]
    
    request_users = requests.Request('GET', GOOGLE_ADMIN_USER_LIST_USERS, params={'access_token': access_token, 'domain': domain, "viewType": 'admin_view'})
    ic(request_users.url)
    prepared_request_users = request_users.prepare()
    response_users = requests.Session().send(prepared_request_users)

    if not response_users.ok:
        raise ValidationError('Failed to obtain user info from Google.')

    user_list = response_users.json()
    ic(user_list)
    
    users_list = []
    for user in user_list["users"]:
        # ic(user)
        if user["primaryEmail"] == admin_user.email:
            continue
        user_record = {
            "email": user["primaryEmail"],
            "picture": user["thumbnailPhotoUrl"] if "thumbnailPhotoUrl" in user.keys() else "",
            "first_name": user["name"]["givenName"],
            "last_name": user["name"]["familyName"],
            "phone": user["phones"][0]["value"] if "phones" in user.keys() else "",
            "emp_from_google": True,
        }     

        # user_record.save()
        users_list.append(user_record)

    
        
        # for email in users["emails"]:
        #     if "primary" in email.keys():
        #         if email["primary"] == True:
    return users_list


def google_validate_admin(*, access_token:  str, user_email: str) -> bool:
    request = requests.Request('GET', GOOGLE_ADMIN_USER_LIST_USERS + "/" + user_email, params={'access_token': access_token, "viewType": 'admin_view'})
    prepared_request = request.prepare()
    response = requests.Session().send(prepared_request)

    if not response.ok:
        return False
    return True


def get_user_id_from_request(request) -> str:
    bearer = request.META.get('HTTP_AUTHORIZATION')
    if bearer:
        token = bearer.split(' ')[1]
        user_id = AccessToken(token)["user_id"]
        return str(user_id)
    return ""