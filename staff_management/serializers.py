from rest_framework import serializers
from .models import Role, Employee

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ["id", "name"]
        
class RoleCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["id", "name"]

class EmployeeSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)

    class Meta:
        model = Employee
        fields = ["id", "name", "role", "employee_id", "email", "password", "dob", "gender", "image", "phone", "address", "city", "state", "zip", "aadhar_no", "aadhar_front_image", "aadhar_back_image", "pan_no", "pan_image", "bank_name", "account_no", "account_holder_name", "ifsc_code", "upi_id", "other1", "other2", "latitude", "longitude", "location", "fees", "last_login", "last_login_ip", "notification_token", "is_active", "plan_id", "plan_expire_date", "otp", "otp_expire", "created_at", "updated_at"]

class EmployeeCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["id", "name", "role", "employee_id", "password", "dob", "gender", "image", "phone", "address", "city", "state", "zip", "aadhar_no", "aadhar_front_image", "aadhar_back_image", "pan_no", "pan_image", "bank_name", "bank_name", "account_no", "account_holder_name", "ifsc_code", "upi_id", "other1", "other2", "latitude", "longitude", "location", "fees", "last_login", "last_login_ip", "notification_token", "is_active", "plan_id", "plan_expire_date", "otp", "otp_expire", "created_at", "updated_at","user"]
        
