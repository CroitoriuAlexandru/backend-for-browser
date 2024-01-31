from django.shortcuts import render
from .models import Company, Department, Employee
from django.contrib.auth.models import User
import requests

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
    
def get_organigram(request):
    context = {}
    if request.method == 'POST':
        print("post request recived")
        user = request.user
        company = Company.objects.get(user=user)
        departments = Department.objects.filter(company=company)
        
        return render(request, 'organigram.html', context)
    else:
        return render(request, 'organigramPage.html', context)