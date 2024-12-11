from .models import IPD,IPDBill 
from rest_framework import serializers


class IPDSerializer(serializers.ModelSerializer):
    class Meta:
        model = IPD
        fields = "__all__"

class IPDCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = IPD
        fields = "__all__"

class IPDBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = IPDBill
        fields = "__all__"

class IPDBillCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = IPDBill
        fields = "__all__"