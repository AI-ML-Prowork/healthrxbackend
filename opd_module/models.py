from django.db import models
from users.models import CustomUser, Tenant
from patients.models import Patient
from staff_management.models import Employee


class OPD(models.Model):
    
    CHARGE_CHOICES = [
        ("OPD Consultation Fees", "OPD Consultation Fees"),
        ("Blood Pressure Check", "Blood Pressure Check"),
        ("Sugar Check", "Sugar Check"),
        ("Other Charges", "Other Charges"),
    ]
    
    PAYMENT_CHOICES = [
        ("Cash", "Cash"),
        ("Transfer to Bank A/C", "Transfer to Bank A/C"),
        ("UPI", "UPI"),
        ("Card", "Card"),
        ("Insurance", "Insurance"),
    ]
    
    CONSULT_CHOICES = [
        ("No", "No"),
        ("Yes", "Yes"),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True) 
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True)
    doctor = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    appointment_date = models.DateField(blank=True, null=True)
    symptoms = models.TextField(blank=True, null=True)
    charge_category = models.CharField(max_length=50, choices=CHARGE_CHOICES, default="OPD Consultation Fees")
    charge = models.CharField(max_length=50, blank=True, null=True)
    payment_mode = models.CharField(max_length=50, choices=PAYMENT_CHOICES, default="Cash")
    paid_amount = models.CharField(max_length=50, blank=True, null=True)
    due_amount = models.CharField(max_length=50, blank=True, null=True)
    live_consult = models.CharField(max_length=5, choices=CONSULT_CHOICES, default="No")
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.user.email})"