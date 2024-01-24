from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# departments table
class Department(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
    
# employee user table
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # on delete set null
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return self.name