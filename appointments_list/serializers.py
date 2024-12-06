from .models import Appointment 
from rest_framework import serializers


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = "__all__"

class AppointmentCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = "__all__"
