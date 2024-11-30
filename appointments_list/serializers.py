from .models import Appointment  # Import the Appointment model
from ambulance.serializers import AmbulanceSerializer,DriverSerializer

class AppointmentSerializer(serializers.ModelSerializer):
    ambulance_details = AmbulanceSerializer(read_only=True, source='ambulance')
    driver_details = DriverSerializer(read_only=True, source='driver')

    class Meta:
        model = Appointment
        fields = "__all__"
