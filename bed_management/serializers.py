from rest_framework import serializers
from .models import BedType, Bed, PatientAssignment

class BedTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BedType
        fields = "__all__"

class BedSerializer(serializers.ModelSerializer):
    bed_type_details = BedTypeSerializer(read_only=True, source='bed_type')

    class Meta:
        model = Bed
        fields = "__all__"

class PatientAssignmentSerializer(serializers.ModelSerializer):
    bed_details = BedSerializer(read_only=True, source='bed')

    class Meta:
        model = PatientAssignment
        fields = "__all__"
