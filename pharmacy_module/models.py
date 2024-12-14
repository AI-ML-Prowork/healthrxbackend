from django.db import models
from users.models import CustomUser, Tenant
from staff_management.models import Employee
from patients.models import Patient


class MedicineList(models.Model):
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True) 
    medicine_name = models.CharField(max_length=255, blank=True, null=True)
    generic_name = models.CharField(max_length=255, blank=True, null=True)
    strength = models.CharField(max_length=255, blank=True, null=True)
    qty = models.CharField(max_length=255, blank=True, null=True)
    box_size = models.CharField(max_length=255, blank=True, null=True)
    units = models.CharField(max_length=255, blank=True, null=True)
    shelf = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    medicine_type = models.CharField(max_length=255, blank=True, null=True)
    image = models.TextField(blank=True, null=True)
    bar_code = models.TextField(blank=True, null=True)
    price = models.CharField(max_length=255, blank=True, null=True)
    vendor = models.CharField(max_length=255, blank=True, null=True)
    manufacturer_name = models.CharField(max_length=255, blank=True, null=True)
    manufacturer_price = models.CharField(max_length=255, blank=True, null=True)
    tax = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateField(auto_now=True, null=True, blank=True)


class PharmacyBill(models.Model):
   
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
    bill_no = models.CharField(max_length=50, blank=True, null=True)
    medicine_category = models.CharField(max_length=50, choices=MEDICINE_CHOICES, default="Tablet")
    medicine_name = models.ForeignKey(MedicineList, on_delete=models.SET_NULL, null=True)
    cost = models.CharField(max_length=10, blank=True, null=True)
    qty = models.CharField(max_length=10, blank=True, null=True)
    amount = models.CharField(max_length=10, blank=True, null=True)
    tax = models.CharField(max_length=10, blank=True, null=True)
    tax_amount = models.CharField(max_length=10, blank=True, null=True)
    discount = models.CharField(max_length=10, blank=True, null=True)
    total_amount = models.CharField(max_length=10, blank=True, null=True)
    subtotal = models.CharField(max_length=10, blank=True, null=True)
    net_amount = models.CharField(max_length=50,blank=True, null=True)
    payment_mode = models.CharField(max_length=50, choices=PAYMENT_CHOICES, default="Cash")
    payment_amount = models.CharField(max_length=50,blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateField(auto_now=True, null=True, blank=True)


class PurchaseMedicine(models.Model):
    
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
    medicine_name = models.ForeignKey(MedicineList, on_delete=models.SET_NULL, null=True)
    medicine_category = models.CharField(max_length=50, choices=MEDICINE_CHOICES, default="Tablet")
    manufacturer_name = models.CharField(max_length=255, blank=True, null=True)
    batch = models.CharField(max_length=255, blank=True, null=True)
    expiry_date = models.CharField(max_length=255, blank=True, null=True)
    mrp = models.CharField(max_length=255, blank=True, null=True)
    batch_amount = models.CharField(max_length=255, blank=True, null=True)
    sale_price = models.CharField(max_length=255, blank=True, null=True)
    packing_qty = models.CharField(max_length=255, blank=True, null=True)
    qty = models.CharField(max_length=255, blank=True, null=True)
    purchase_amount = models.CharField(max_length=10, blank=True, null=True)
    tax = models.CharField(max_length=10, blank=True, null=True)
    tax_amount = models.CharField(max_length=10, blank=True, null=True)
    total_amount = models.CharField(max_length=10, blank=True, null=True)
    subtotal = models.CharField(max_length=10, blank=True, null=True)
    discount = models.CharField(max_length=10, blank=True, null=True)
    net_amount = models.CharField(max_length=50,blank=True, null=True)
    payment_mode = models.CharField(max_length=50, choices=PAYMENT_CHOICES, default="Cash")
    payment_amount = models.CharField(max_length=50,blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateField(auto_now=True, null=True, blank=True)