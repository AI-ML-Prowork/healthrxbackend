from django.db import models
from users.models import CustomUser, Tenant
from patients.models import Patient
from staff_management.models import Employee


class IPD(models.Model):
    
    CASUALTY_CHOICES = [
        ("No", "No"),
        ("Yes", "Yes"),
    ]
    
    CONSULT_CHOICES = [
        ("No", "No"),
        ("Yes", "Yes"),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True) 
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True)
    doctor = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    height = models.CharField(max_length=10, blank=True, null=True)
    bp = models.CharField(max_length=10, blank=True, null=True)
    pulse = models.CharField(max_length=10, blank=True, null=True)
    temperature = models.CharField(max_length=10, blank=True, null=True)
    respiration = models.CharField(max_length=10, blank=True, null=True)
    symptoms = models.TextField(blank=True, null=True)
    previous_medical_issue = models.TextField(blank=True, null=True)
    bed_no = models.CharField(max_length=10, blank=True, null=True)
    ward = models.CharField(max_length=10, blank=True, null=True)
    floor = models.CharField(max_length=10, blank=True, null=True)
    casualty = models.CharField(max_length=5, choices=CASUALTY_CHOICES, default="No")
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.user.email})"
    
class IPDBill(models.Model):
    
    PAYMENT_CHOICES = [
        ("Cash", "Cash"),
        ("Transfer to Bank A/C", "Transfer to Bank A/C"),
        ("UPI", "UPI"),
        ("Card", "Card"),
        ("Insurance", "Insurance"),
    ]
    
    MEDICINE_CHOICES = [
        ("Consultation Charges", "Consultation Charges"),   
        ("Pathology Charges", "Pathology Charges"),   
        ("Radiology Charges", "Radiology Charges"),   
        ("Misc.Charges", "Misc.Charges"),   
        ("Tablet", "Tablet"),   
        ("Syrup", "Syrup"),   
        ("Capsule", "Capsule"),   
        ("Injection", "Injection"),   
        ("Ointment", "Ointment"),   
        ("Cream", "Cream"),   
        ("Surgical", "Surgical"),   
        ("Drops", "Drops"),   
        ("Inhalers", "Inhalers"),   
        ("Implants / Patches", "Implants / Patches"),   
        ("Liquid", "Liquid"),   
        ("Preparations", "Preparations"),   
        ("Diaper", "Diaper"),
    ]   
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True) 
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True)
    doctor = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    medicine_category = models.CharField(max_length=50, choices=MEDICINE_CHOICES, default="Tablet")
    medicine_name = models.CharField(max_length=10, blank=True, null=True)
    cost = models.CharField(max_length=10, blank=True, null=True)
    qty = models.CharField(max_length=10, blank=True, null=True)
    amount = models.CharField(max_length=10, blank=True, null=True)
    tax = models.CharField(max_length=10, blank=True, null=True)
    tax_amount = models.CharField(max_length=10, blank=True, null=True)
    discount = models.CharField(max_length=10, blank=True, null=True)
    total_amount = models.CharField(max_length=10, blank=True, null=True)
    subtotal = models.CharField(max_length=10, blank=True, null=True)
    payment_mode = models.CharField(max_length=50, choices=PAYMENT_CHOICES, default="Cash")
    net_amount = models.CharField(max_length=50, blank=True, null=True)
    paid_amount = models.CharField(max_length=50, blank=True, null=True)
    due_amount = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.user.email})"