from .models import Radiology,RadiologyBill 
from rest_framework import serializers


class RadiologySerializer(serializers.ModelSerializer):
    class Meta:
        model = Radiology
        fields = "__all__"

class RadiologyCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Radiology
        fields = "__all__"

class RadiologyBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = RadiologyBill
        fields = "__all__"

class RadiologyBillCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RadiologyBill
        fields = "__all__"