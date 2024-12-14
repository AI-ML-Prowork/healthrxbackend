from .models import MedicineList,PharmacyBill,PurchaseMedicine
from rest_framework import serializers


class MedicineListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineList
        fields = "__all__"

class MedicineListCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineList
        fields = "__all__"

class PharmacyBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = PharmacyBill
        fields = "__all__"

class PharmacyBillCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PharmacyBill
        fields = "__all__"
        
class PurchaseMedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseMedicine
        fields = "__all__"

class PurchaseMedicineCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseMedicine
        fields = "__all__"