from django.db import models
from users.models import CustomUser, Tenant
from patients.models import Patient
from staff_management.models import Employee


class Radiology(models.Model):
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True) 
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True)
    test_type = models.CharField(max_length=50, blank=True, null=True)
    test_name = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=10, blank=True, null=True)
    sub_category = models.CharField(max_length=10, blank=True, null=True)
    method = models.CharField(max_length=10, blank=True, null=True)
    report_time = models.CharField(max_length=10, blank=True, null=True)
    charge_name = models.CharField(max_length=10, blank=True, null=True)
    charge_amount = models.CharField(max_length=10, blank=True, null=True)
    tax = models.TextField(blank=True, null=True)
    total_amount = models.TextField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.user.email})"
    
class RadiologyBill(models.Model):
    
    PAYMENT_CHOICES = [
        ("Cash", "Cash"),
        ("Transfer to Bank A/C", "Transfer to Bank A/C"),
        ("UPI", "UPI"),
        ("Card", "Card"),
        ("Insurance", "Insurance"),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True) 
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True)
    doctor = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    bill_no = models.CharField(max_length=50, blank=True, null=True)
    test_name = models.CharField(max_length=100, blank=True, null=True)
    report_time = models.CharField(max_length=10, blank=True, null=True)
    amount = models.CharField(max_length=10, blank=True, null=True)
    discount = models.CharField(max_length=10, blank=True, null=True)
    tax = models.TextField(blank=True, null=True)
    net_amount = models.TextField(blank=True, null=True)
    payment_mode = models.CharField(max_length=50, choices=PAYMENT_CHOICES, default="Cash")
    payment_amount = models.TextField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.user.email})"