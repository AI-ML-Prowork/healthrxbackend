from django.db import models
from users.models import CustomUser, Tenant
from patients.models import Patient
from staff_management.models import Employee


class Billing(models.Model):
    
    BILL_CHOICES = [
        ("Consultation", "Consultation"),
        ("Admission", "Admission"),
        ("OPD", "OPD"),
        ("IPD", "IPD"),
        ("Appointment", "Appointment"),
        ("Pharmacy", "Pharmacy"),
        ("Pathology", "Pathology"), 
        ("Radiology", "Radiology"), 
        ("Operation", "Operation"), 
    ]
    
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
    bill_type = models.CharField(max_length=50, choices=BILL_CHOICES, default="Consultation")
    amount = models.CharField(max_length=50, blank=True, null=True)
    amount_due = models.CharField(max_length=50, blank=True, null=True)
    payment_mode = models.CharField(max_length=50, choices=PAYMENT_CHOICES, default="Cash")
    billing_address = models.TextField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.user.email})"