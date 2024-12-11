from .models import Pathology,PathologyBill 
from rest_framework import serializers


class PathologySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pathology
        fields = "__all__"

class PathologyCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pathology
        fields = "__all__"

class PathologyBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = PathologyBill
        fields = "__all__"

class PathologyBillCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PathologyBill
        fields = "__all__"