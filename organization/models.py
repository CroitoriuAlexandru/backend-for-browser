from django.db import models
from authentication.models import User



# employee user table
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    company = models.ForeignKey('Company', on_delete=models.CASCADE, null=True, blank=True)
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, blank=True)
    supervizer_id = models.CharField(max_length=200, null=True, blank=True)
    emp_from_google = models.BooleanField(default=False)
    picture = models.URLField(null=True, blank=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    
    
    REGISTRATION_CHOICES = [
        ('ceo', 'CEO'),
        ('employee', 'Employee'),
    ]

    registration_method = models.CharField(
        max_length=10,
        choices=REGISTRATION_CHOICES,
        default='email'
    )

    @property
    def department_name(self):
        return self.department.name

    def __str__(self):
        return self.first_name + ' ' + self.last_name


# organization table
class Company(models.Model):
    ceo = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    api_record_id = models.CharField(max_length=200, null=True, blank=True)
    last_querry_date = models.CharField(max_length=200, null=True, blank=True)
    cui = models.CharField(max_length=200, null=True, blank=True)
    nr_employees = models.CharField(max_length=200, null=True, blank=True)
    denumire = models.CharField(max_length=200, null=True, blank=True)
    adresa = models.CharField(max_length=200, null=True, blank=True)
    nrRegCom = models.CharField(max_length=200, null=True, blank=True)
    telefon = models.CharField(max_length=200, null=True, blank=True)
    fax = models.CharField(max_length=200, null=True, blank=True)
    codPostal = models.CharField(max_length=200, null=True, blank=True)
    act = models.CharField(max_length=200, null=True, blank=True)
    stare_inregistrare = models.CharField(max_length=200, null=True, blank=True)
    data_inregistrare = models.CharField(max_length=200, null=True, blank=True)
    cod_CAEN = models.CharField(max_length=200, null=True, blank=True)
    iban = models.CharField(max_length=200, null=True, blank=True)
    statusRO_e_Factura = models.CharField(max_length=200, null=True, blank=True)
    organFiscalCompetent = models.CharField(max_length=200, null=True, blank=True)
    forma_de_proprietate = models.CharField(max_length=200, null=True, blank=True)
    forma_organizare = models.CharField(max_length=200, null=True, blank=True)
    forma_juridica = models.CharField(max_length=200, null=True, blank=True)
    
    def __str__(self):
        return f'{self.denumire}'


# departments table
class Department(models.Model):
    company = models.ForeignKey('Company', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f'{self.name}'
 
    def get_employees(self):
        return Employee.objects.filter(department=self)
 