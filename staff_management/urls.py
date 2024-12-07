from django.urls import path
from .views import *

urlpatterns = [
    path("roles", RoleView.as_view(), name="roles-list"),
    path("roles/<int:role_id>", RoleManagementView.as_view(), name="role-manage"),
    path("employees", EmployeeListView.as_view(), name="employees-list"),
    path("employees/<int:employee_id>", EmployeeManagementView.as_view(), name="employee-manage"),

]
