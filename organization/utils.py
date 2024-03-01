from authentication.utils import google_get_user_list
from authentication.utils import get_user_id_from_request
from authentication.models import User
from organization.models import Company, Department, Employee
from authentication.serializers import UserSerializer
from icecream import ic

def organigram_info(request):
    user_id = get_user_id_from_request(request)
    userSerializer = UserSerializer
    user_serializer = userSerializer(User.objects.get(id=user_id), many=False)
    departments = Department.objects.filter(company__ceo_id=user_id)

    employees = Employee.objects.filter(company__ceo_id=user_id)
    ic(employees)
    employees_data = []
    for employee in employees:
        employee_data = {
            "id": employee.id,
            "user_id": employee.user_id,
            "company_id": employee.company_id,
            "department_id": employee.department_id,
            "department_name": employee.department_name,
            "emp_from_google": employee.emp_from_google,
            "picture": employee.picture,
            "first_name": employee.first_name,
            "last_name": employee.last_name,
            "phone": employee.phone,
            "email": employee.email
        }
        employees_data.append(employee_data)
    data = {
        "ceo": user_serializer.data,
        "departments": departments.values(),
        "employees": employees_data
    }
    
    return data


# fields = ['user_id', 'company_id', 'department_id', "department_name", 'emp_from_google', 'picture', 'first_name', 'last_name', 'phone', 'email']
