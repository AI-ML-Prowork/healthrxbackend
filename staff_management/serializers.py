from rest_framework import serializers
from .models import Role, Employee

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ["id", "name"]

class EmployeeSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)

    class Meta:
        model = Employee
        fields = ["id", "name", "email", "phone", "address", "role", "date_of_joining"]

class EmployeeCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["name", "email", "phone", "address", "role", "date_of_joining"]
