from django.db import models
from users.models import CustomUser, Tenant
from patients.models import Patient
from staff_management.models import Employee


class Appointment(models.Model):
    
    PRIORITY_CHOICES = [
        ("Normal", "Normal"),
        ("High", "High"),
        ("Very High", "Very High"),
        ("Low", "Low"),
    ]
    
    SHIFT_CHOICES = [
        ("Morning", "Morning"),
        ("Evening", "Evening"),
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
    name = models.CharField(max_length=100, default="test")
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True)
    doctor = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    fees = models.CharField(max_length=5, unique=True, null=True)
    shift = models.CharField(max_length=50, choices=SHIFT_CHOICES, default="Morning")
    appointment_date = models.DateField(blank=True, null=True)
    priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES, default="Normal")
    payment_mode = models.CharField(max_length=50, choices=PAYMENT_CHOICES, default="Cash")
    live_consult = models.CharField(max_length=5, choices=CONSULT_CHOICES, default="No")
    address = models.TextField(blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.user.email})"