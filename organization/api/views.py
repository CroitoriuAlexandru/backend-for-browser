from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

import re # regex
import requests

# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from rest_framework_simplejwt.views import TokenObtainPairView

from organization.models import Company
from organization.serializer import CompanySerializer

def validateCui(cui):
    # Check if cui is None or empty
    if cui is None or cui == '':
        return False

    # Check if cui contains only numbers
    if re.fullmatch(r'\d*', cui):
        return False

    return True


# @permission_classes([IsAuthenticated])
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def set_organization(request):
    # print(request.data["cui"])
    cui = request.data["cui"]
    # cui must be validated to not be empty and to only contain numbers
    if not validateCui(cui):
        print("cui is not valid")
        return Response({"message": "CUI is not valid"}, status=400)
    
    user = request.user

    if Company.objects.filter(user_id=user.id).exists():
        company = Company.objects.get(user_id=user.id, cui=cui)
        serializer = CompanySerializer(company, many=False)
        return Response(serializer.data) 

    endpoint = f"https://api.aipro.ro/get?cui={cui}"
    response = requests.get(endpoint)
    print(cui)
    print(user)
    
    if response.status_code != 200:
        return Response({"message": "Invalid CUI"}, status=400)
    
    organization_data = {
        "user_id": user.id,
        "api_record_id": response.json().get("_id"),
        "last_querry_date": response.json().get("date_generale").get("data"),
        "cui": response.json().get("CUI"),
        "denumire": response.json().get("nume_companie"),
        "adresa": response.json().get("date_generale").get("adresa"),
        "nrRegCom": response.json().get("date_generale").get("nrRegCom"),
        "telefon": response.json().get("date_generale").get("telefon"),
        "fax": response.json().get("date_generale").get("fax"),
        "codPostal": response.json().get("date_generale").get("codPostal"),
        "act": response.json().get("date_generale").get("act"),
        "stare_inregistrare": response.json().get("date_generale").get("stare_inregistrare"),
        "data_inregistrare": response.json().get("date_generale").get("data_inregistrare"),
        "cod_CAEN": response.json().get("date_generale").get("cod_CAEN"),
        "iban": response.json().get("date_generale").get("iban"),
        "statusRO_e_Factura": response.json().get("date_generale").get("statusRO_e_Factura"),
        "organFiscalCompetent": response.json().get("date_generale").get("organFiscalCompetent"),
        "forma_de_proprietate": response.json().get("date_generale").get("forma_de_proprietate"),
        "forma_organizare": response.json().get("date_generale").get("forma_organizare"),
        "forma_juridica": response.json().get("date_generale").get("forma_juridica"),
    }
    company = Company(**organization_data)
    company.save()


    # company_data = Company.objects.first()
    serializer = CompanySerializer(company, many=False)
    print(serializer.data)
    return Response(serializer.data)
    

@api_view(['GET'])
def generate_departments(request):
    data = {
        'departments': [
            'sales',
            'marketing',
            'finance',
            'hr',
            'it',
        ]
    }
    return Response(data)



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
