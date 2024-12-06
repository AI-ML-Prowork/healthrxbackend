from .models import Billing 
from rest_framework import serializers


class BillingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Billing
        fields = "__all__"

class BillingCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Billing
        fields = "__all__"
