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

from organization.models import Company, Department, Employee
from organization.serializers import CompanySerializer, DepartmentSerializer, EmployeeSerializer
from organization.ai.gptdepartamente import generate_departments
from authentication.serializers import UserSerializer
from authentication.utils import google_get_user_list
from organization.utils import organigram_info
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
            "ceo_id": user.id,
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
    user_company = Company.objects.filter(ceo_id=user.id)
    if user_company.exists():
        company = user_company.first()
        company.delete()
        organization_data = get_company_info(user, cui)
        if organization_data.get("message"):
            return Response(organization_data, status=200)
        user_company = Company(**organization_data)
        user_company.save()
        deparment_unasigned = Department(company=user_company, name="unasigned")
        deparment_unasigned.save()
        serializer = CompanySerializer(company, many=False)
    else:
        organization_data = get_company_info(user, cui)
        if organization_data.get("message"):
            return Response(organization_data, status=200)
        user_company = Company(**organization_data)
        user_company.save()
        deparment_unasigned = Department(company=user_company, name="unasigned")
        deparment_unasigned.save()
        serializer = CompanySerializer(company, many=False)
        
    user_company = Company.objects.filter(ceo_id=user.id)

    users_list = google_get_user_list(admin_id=user.id)
    # ic(users_list)


    for user in users_list:
        employee = Employee(
            company_id=user_company.first().id,
            email=user["email"],
            picture=user["picture"],
            first_name=user["first_name"],
            last_name=user["last_name"],
            phone=user["phone"],
            department_id=deparment_unasigned.id,
            emp_from_google=True
        )
        employee.save()

    return Response(serializer.data, status=200)


#  company classes
class get_organigram_info(PublicApiMixin, ApiErrorsMixin, APIView):
    userSerializer = UserSerializer

    def get(self, request, *args, **kwargs):
        data = organigram_info(request)
        return Response(data, status=200)

class set_employee_department(PublicApiMixin, ApiErrorsMixin, APIView):
        
        def post(self, request, *args, **kwargs):
            user = get_user_id_from_request(request)
            company = Company.objects.filter(ceo_id=user)
            if not company.exists():
                return Response({"message": "Company not found for this user"}, status=200)
            
            employee = Employee.objects.filter(id=request.data.get("employee_id"))
            if not employee.exists():
                return Response({"message": "Employee not found"}, status=200)
            
            department = Department.objects.filter(id=request.data.get("department_id"))
            if not department.exists():
                return Response({"message": "Department not found"}, status=200)
            
            employee.update(department=department.first())

            data = organigram_info(request)
            return Response(data, status=200)

class generate_company_departments(PublicApiMixin, ApiErrorsMixin, APIView):
    
    def get(self, request, *args, **kwargs):
        user = get_user_id_from_request(request)
        company = Company.objects.filter(ceo_id=user)
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
        company = Company.objects.filter(ceo_id=user)
        if not company.exists():
            return Response({"message": "Company not found for this user"}, status=200)
        
        cod_CAEN = request.data.get("cod_CAEN")
        company.update(cod_CAEN=cod_CAEN)
        serializer = CompanySerializer(company.first(), many=False)
        return Response(serializer.data, status=200)


class set_nr_employees(PublicApiMixin, ApiErrorsMixin, APIView):
    
    def post(self, request, *args, **kwargs):
        user = get_user_id_from_request(request)
        company = Company.objects.filter(ceo_id=user)
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
        company = Company.objects.filter(ceo_id=user)
        if not company.exists():
            return Response({"message": "Company not found for this user"}, status=200)
        
        dbo_departments = Department.objects.filter(company=company.first())

        for department in dbo_departments:
            if department.name != "unasigned":
                department.delete()
        
        r_departments = request.data.get("departments")
        
        for department in r_departments:
            new_department = Department(company=company.first(), name=department)
            new_department.save()

        deparmentsSerilizer = DepartmentSerializer(Department.objects.filter(company=company.first()), many=True)
        
        return Response(deparmentsSerilizer.data, status=200)