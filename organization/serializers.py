from rest_framework import serializers
from organization.models import *

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = (
            'ceo',
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
        
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['user_id', 'company_id', 'department_id', "department_name", 'emp_from_google', 'picture', 'first_name', 'last_name', 'phone', 'email']
            