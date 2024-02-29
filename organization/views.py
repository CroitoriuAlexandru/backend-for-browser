from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from authentication.utils import get_user_id_from_request
from authentication.models import User
import re # regex
import requests
from icecream import ic
from authentication.mixins import PublicApiMixin, ApiErrorsMixin
from rest_framework.views import APIView
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from rest_framework_simplejwt.views import TokenObtainPairView
import json

from organization.models import Company, Department
from organization.serializer import CompanySerializer, DepartmentSerializer
from organization.ai.gptdepartamente import generate_departments

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
            "nr_employees": response.json().get("an2022").get("i")[0].get("val_indicator"),
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
   
    user = User.objects.get(id=get_user_id_from_request(request))
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


# @api_view(['GET'])
# def generate_company_departments(request):
#     print("test")

#     data = generate_departments("19", "5")

#     # user = request.user
#     # print(user)
#     # if user.is_anonymous:
#     #     return Response({"message": "User not found"}, status=200)


#     # data = {
#     #     'departments': [
#     #         'sales',
#     #         'marketing',
#     #         'finance',
#     #         'hr',
#     #         'it',
#     #     ]
#     # }
    
#     # fetch_company_info()
#     ic(data)
#     return Response(data)

class generate_company_departments(PublicApiMixin, ApiErrorsMixin, APIView):
    
    def get(self, request, *args, **kwargs):
        user = get_user_id_from_request(request)
        company = Company.objects.filter(user_id=user)
        if not company.exists():
            return Response([{"message": "Company not found for this user"}], status=200)
        
        cod_caen = company.first().cod_CAEN
        nr_employees = company.first().nr_employees
        
        
        ic(type(cod_caen))
        ic(type(nr_employees))
        data = generate_departments(cod_caen, nr_employees)
        ic(data)
        return Response(json.loads(data))


class set_caen_code(PublicApiMixin, ApiErrorsMixin, APIView):
    
    def post(self, request, *args, **kwargs):
        user = get_user_id_from_request(request)
        company = Company.objects.filter(user_id=user)
        if not company.exists():
            return Response({"message": "Company not found for this user"}, status=200)
        
        cod_CAEN = request.data.get("cod_CAEN")
        company.update(cod_CAEN=cod_CAEN)
        serializer = CompanySerializer(company.first(), many=False)
        return Response(serializer.data, status=200)


class set_nr_employees(PublicApiMixin, ApiErrorsMixin, APIView):
    
    def post(self, request, *args, **kwargs):
        user = get_user_id_from_request(request)
        company = Company.objects.filter(user_id=user)
        if not company.exists():
            return Response({"message": "Company not found for this user"}, status=200)
        
        nr_employees = request.data.get("nr_employees")
        ic(nr_employees)
        company.update(nr_employees=nr_employees)
        ic(company.first().nr_employees)
        serializer = CompanySerializer(company.first(), many=False)
        return Response(serializer.data, status=200)
    
class set_company_departments(PublicApiMixin, ApiErrorsMixin, APIView):
    
    def post(self, request, *args, **kwargs):
        user = get_user_id_from_request(request)
        company = Company.objects.filter(user_id=user)
        if not company.exists():
            return Response({"message": "Company not found for this user"}, status=200)
        
        dbo_departments = Department.objects.filter(company=company.first())
        dbo_departments.delete()
        
        r_departments = request.data.get("departments")
        
        for department in r_departments:
            new_department = Department(company=company.first(), name=department)
            new_department.save()

        deparmentsSerilizer = DepartmentSerializer(Department.objects.filter(company=company.first()), many=True)
        
        return Response(deparmentsSerilizer.data, status=200)