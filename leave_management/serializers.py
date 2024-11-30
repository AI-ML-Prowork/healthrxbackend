from rest_framework import serializers
from .models import LeaveRequest, LeaveType, Employee

class LeaveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveType
        fields = "__all__"

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"

class LeaveRequestSerializer(serializers.ModelSerializer):
    employee_details = EmployeeSerializer(read_only=True, source='employee')
    leave_type_details = LeaveTypeSerializer(read_only=True, source='leave_type')

    class Meta:
        model = LeaveRequest
        fields = "__all__"
