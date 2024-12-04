from rest_framework import serializers
from .models import Patient

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ["patient_id", "name", "phone", "guardian_name", "age", "gender", "blood_group", "marital_status","department", "email", "address", "city", "state", "zip", "allergies", "remarks", "tpa_id", "tpa_validity", "identity_no", "created_at", "updated_at"]
