from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Role, Employee
from .serializers import RoleSerializer, EmployeeSerializer, EmployeeCreateUpdateSerializer
from clients.custom_permissions import IsTenantAdminOrIsUserPartOfTenant
import logging
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError

logger = logging.getLogger(__name__)

class RoleView(APIView):
    permission_classes = [IsAuthenticated, IsTenantAdminOrIsUserPartOfTenant]

    def get(self, request):
        roles = Role.objects.filter(tenant=request.tenant)
        serializer = RoleSerializer(roles, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(tenant=request.tenant)
            return Response({"msg": "Role added successfully!"}, status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class EmployeeListView(APIView):
    permission_classes = [IsAuthenticated, IsTenantAdminOrIsUserPartOfTenant]

    # GET: List all employees for the tenant
    def get(self, request):
        employees = Employee.objects.filter(tenant=request.tenant)
        serializer = EmployeeSerializer(employees, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    # POST: Add a new employee
    def post(self, request):
        serializer = EmployeeCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Save employee with user and tenant
                serializer.save(user=request.user, tenant=request.tenant)
                return Response({"msg": "Employee added successfully!"}, status=status.HTTP_201_CREATED)
            except IntegrityError as e:
                raise ValidationError({"error": str(e)})
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



class EmployeeManagementView(APIView):
    permission_classes = [IsAuthenticated, IsTenantAdminOrIsUserPartOfTenant]

    def get(self, request, employee_id):
        try:
            employee = Employee.objects.get(id=employee_id, tenant=request.tenant)
            serializer = EmployeeSerializer(employee)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        except Employee.DoesNotExist:
            return Response({"msg": "Employee not found."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = EmployeeCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(tenant=request.tenant)
            return Response({"msg": "Employee added successfully!"}, status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, employee_id):
        try:
            employee = Employee.objects.get(id=employee_id, tenant=request.tenant)
            serializer = EmployeeCreateUpdateSerializer(employee, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"msg": "Employee updated successfully!"}, status=status.HTTP_200_OK)
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Employee.DoesNotExist:
            return Response({"msg": "Employee not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, employee_id):
        try:
            employee = Employee.objects.get(id=employee_id, tenant=request.tenant)
            employee.delete()
            return Response({"msg": "Employee deleted successfully!"}, status=status.HTTP_200_OK)
        except Employee.DoesNotExist:
            return Response({"msg": "Employee not found."}, status=status.HTTP_404_NOT_FOUND)
