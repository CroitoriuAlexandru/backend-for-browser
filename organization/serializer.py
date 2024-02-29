from rest_framework import serializers
from organization.models import *

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = (
            'user',
            'api_record_id',
            'last_querry_date',
            'cui',
            "nr_employees",
            'denumire',
            'adresa',
            'nrRegCom',
            'telefon',
            'fax',
            'codPostal',
            'act',
            'stare_inregistrare',
            'data_inregistrare',
            'cod_CAEN',
            'iban',
            'statusRO_e_Factura',
            'organFiscalCompetent',
            'forma_de_proprietate',
            'forma_organizare',
            'forma_juridica'
            )
        
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['name']
            