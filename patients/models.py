from django.db import models
from users.models import CustomUser, Tenant
from staff_management.models import Employee


class Patient(models.Model):
    
    BLOOD_GROUP_CHOICES = [
        ("A+", "A+"),
        ("A+", "A+"),
        ("B+", "B+"),
        ("A-", "A-"),
        ("B-", "B-"),
        ("AB+", "AB+"),
        ("AB-", "AB-"),
        ("O+", "O+"),
        ("O-", "O-"),
    ]
    
    MARITAL_STATUS_CHOICES = [
        ("Single", "Single"),
        ("Married", "Married"),
        ("Widowed", "Widowed"),
        ("Separated", "Separated"),
        ("Not Specified", "Not Specified"),
    ]
    
    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
        ("Not Specified", "Not Specified"),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True) 
    patient_id = models.CharField(max_length=100, unique=True, null=True)
    name = models.CharField(max_length=100, default="test")
    phone = models.CharField(max_length=15, unique=True, null=True)
    guardian_name = models.CharField(max_length=50, null=True)
    guardian_phone = models.CharField(max_length=15, null=True)
    age = models.CharField(max_length=3, default="0")
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES, default="Not Specified")
    doctor = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, default="A+")
    marital_status = models.CharField(max_length=15, choices=MARITAL_STATUS_CHOICES, default="Not Specified")
    image = models.TextField(blank=True, null=True)
    department = models.CharField(max_length=50, null=True)
    email = models.EmailField(max_length=100, unique=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=50, null=True)
    zip = models.CharField(max_length=10, null=True)
    allergies = models.TextField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    tpa_id = models.CharField(max_length=50, null=True, blank=True)
    tpa_validity = models.CharField(max_length=50, null=True, blank=True)
    identity_no = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.user.email})"