from .models import OPD 
from rest_framework import serializers


class OPDSerializer(serializers.ModelSerializer):
    class Meta:
        model = OPD
        fields = "__all__"

class OPDCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OPD
        fields = "__all__"
