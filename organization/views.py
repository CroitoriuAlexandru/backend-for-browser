from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
# from organization.ai.department_generator import fetch_company_info

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
    if re.search(r'[a-zA-Z]', cui):
        return False

    return True


def get_company_info(user, cui):
    
    if not validateCui(cui):
        print("cui is not valid")
        return {"message": "CUI is not valid"}
    
    endpoint = f"https://api.aipro.ro/get?cui={cui}"
    response = requests.get(endpoint)
    if response.status_code != 200:
        return {"message": 'Company with cui {cui} not found'}



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


    return organization_data

# @permission_classes([IsAuthenticated])
# @permission_classes([IsAuthenticated])
@api_view(['POST'])
def set_organization(request):
    cui = request.data["cui"]
    # cui must be validated to not be empty and to only contain numbers
   
    user = request.user
    if user.is_anonymous:
        return Response({"message": "User not found"}, status=200)

    #  user has a company and it will return it
    user_company = Company.objects.filter(user_id=user.id)
    if user_company.exists():
        company = user_company.first()
        company.delete()
        organization_data = get_company_info(user, cui)
        if organization_data.get("message"):
            return Response(organization_data, status=200)
        company = Company(**organization_data)
        company.save()
        serializer = CompanySerializer(company, many=False)
        return Response(serializer.data)
    else:
        organization_data = get_company_info(user, cui)
        if organization_data.get("message"):
            return Response(organization_data, status=200)
        company = Company(**organization_data)
        company.save()
        serializer = CompanySerializer(company, many=False)
        return Response(serializer.data)


@api_view(['GET'])
def generate_departments(request):

    user = request.user
    print(user)
    if user.is_anonymous:
        return Response({"message": "User not found"}, status=200)


    data = {
        'departments': [
            'sales',
            'marketing',
            'finance',
            'hr',
            'it',
        ]
    }
    # fetch_company_info()
    return Response(data)


@api_view(['GET'])
def get_mails(request):
    data = {
        "mails": [
            {
                "name": "John Doe",
                "email": "jhon_doe@gmail.com"
            },
            {
                "name": "Coana Mare",
                "email": "coana_mare@gmail.com"
            },
            {
                "name": "Gigi Becali",
                "email": "gigi_becali@gmail.com"
            },
            {
                "name": "Baga Hagi",
                "email": "baga_hagi@gmail.com"
            },
            {
                "name": "Testul Test",
                "email": "testul_test@gmail.com"
            }
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