from django.shortcuts import render, redirect
from .models import Company, Department, Employee
from django.contrib.auth.models import User
import requests

def getCompanyContext(user):
    company = Company.objects.get(user=user)
    employees = Employee.objects.filter(company=company)
    departments = Department.objects.filter(company=company)
    context = {
        'company': company,
        'employees': employees,
        'departments': departments,
    }
    return context


# Create your views here.
def get_organization_data(cui, user):
    endpoint = f"https://api.aipro.ro/get?cui={cui}"
    response = requests.get(endpoint)
    organization_data = {
        "user": user,
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


# create a view that recives a string and makes a request for the api
def registerOrganization(request):
    if request.method == 'POST':
        cui = request.POST.get('cui')
        print(cui)
        company = Company.objects.filter(cui=cui)
        if not company.exists():
            organization_data = get_organization_data(cui, request.user)
            company = Company(**organization_data)
            company.save()

        print(company)
        return render(request, 'organization.html', {'company': company})
    
    else :
        return render(request, 'organization.html', {'cui': "Enter CUI"})

def organigramPage(request):
    user = request.user
    company = Company.objects.get(user=user)
    context = getCompanyContext(user)
    if request.method == 'POST':
        print("poist request should not be allowed")
        return render(request, 'organigramPage.html', context)
    else:
        return render(request, 'organigramPage.html', context)
    
    

def create_employee(request):
    user = request.user
    company = Company.objects.get(user=user)
    context = {
        "company": company,
    }
    if request.method == 'POST':
        print("post request recived")
        
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = User.objects.create_user(username, email, password)
        user.save()
        employee = Employee(user=user, company=company)
        employee.save()

    context = getCompanyContext(request.user)
    return render(request, 'employees.html', context)

def delete_employee(request, pk):
    user = User.objects.get(id=pk)
    user.delete()

    context = getCompanyContext(request.user)
    return render(request, 'employees.html', context) 

def create_department(request):
    user = request.user
    company = Company.objects.get(user=user)
    if request.method == 'POST':
        print("post request recived")
        name = request.POST.get('department')        
        department = Department(company=company, name=name)
        department.save()
        
    context = getCompanyContext(user)
    return render(request, 'departments.html', context)


def delete_department(request, pk):
    department = Department.objects.get(id=pk)
    department.delete()

    context = getCompanyContext(request.user)
    return render(request, 'departments.html', context)