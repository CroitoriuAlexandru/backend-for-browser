from django.shortcuts import render
from .models import Company
import requests
# Create your views here.

# create a view that recives a string and makes a request for the api
def registerOrganization(request):
    if request.method == 'POST':
        endpoint = "https://api.aipro.ro/get?cui="
        cui = request.POST.get('cui')
        print(cui)
        url = endpoint + cui
        print(url)
        response = requests.get(url)
        # if response is not 200 return just the cui that was recived
        print(response.json().get("date_generale"))
        api_record_id = response.json().get("_id")
        last_querry_date = response.json().get("date_generale").get("data")
        cui = response.json().get("CUI")
        denumire = response.json().get("nume_companie")
        adresa = response.json().get("date_generale").get("adresa")
        nrRegCom = response.json().get("date_generale").get("nrRegCom")
        telefon = response.json().get("date_generale").get("telefon")
        fax = response.json().get("date_generale").get("fax")
        codPostal = response.json().get("date_generale").get("codPostal")
        act = response.json().get("date_generale").get("act")
        stare_inregistrare = response.json().get("date_generale").get("stare_inregistrare")
        data_inregistrare = response.json().get("date_generale").get("data_inregistrare")
        cod_CAEN = response.json().get("date_generale").get("cod_CAEN")
        iban = response.json().get("date_generale").get("iban")
        statusRO_e_Factura = response.json().get("date_generale").get("statusRO_e_Factura")
        organFiscalCompetent = response.json().get("date_generale").get("organFiscalCompetent")
        forma_de_proprietate = response.json().get("date_generale").get("forma_de_proprietate")
        forma_organizare = response.json().get("date_generale").get("forma_organizare")
        forma_juridica = response.json().get("date_generale").get("forma_juridica")
        organization_data = {
            "api_record_id": api_record_id,
            "last_querry_date": last_querry_date,
            "cui": cui,
            "denumire": denumire,
            "adresa": adresa,
            "nrRegCom": nrRegCom,
            "telefon": telefon,
            "fax": fax,
            "codPostal": codPostal,
            "act": act,
            "stare_inregistrare": stare_inregistrare,
            "data_inregistrare": data_inregistrare,
            "cod_CAEN": cod_CAEN,
            "iban": iban,
            "statusRO_e_Factura": statusRO_e_Factura,
            "organFiscalCompetent": organFiscalCompetent,
            "forma_de_proprietate": forma_de_proprietate,
            "forma_organizare": forma_organizare,
            "forma_juridica": forma_juridica,
        }
        print(organization_data)
        company = Company(**organization_data)
        company.save()
        
        context = {
            'cui': cui,
            'response': company,
        }
        return render(request, 'organization.html', context)
    
    else :
        return render(request, 'organization.html', {'response': "test"})