# Generated by Django 4.2.16 on 2024-12-11 12:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("patients", "0007_alter_patient_user"),
        ("users", "0001_initial"),
        ("staff_management", "0008_alter_employee_user"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="IPDBill",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "medicine_category",
                    models.CharField(
                        choices=[
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
                        ],
                        default="Tablet",
                        max_length=50,
                    ),
                ),
                (
                    "medicine_name",
                    models.CharField(blank=True, max_length=10, null=True),
                ),
                ("cost", models.CharField(blank=True, max_length=10, null=True)),
                ("amount", models.CharField(blank=True, max_length=10, null=True)),
                ("tax", models.CharField(blank=True, max_length=10, null=True)),
                ("tax_amount", models.CharField(blank=True, max_length=10, null=True)),
                ("discount", models.CharField(blank=True, max_length=10, null=True)),
                (
                    "total_amount",
                    models.CharField(blank=True, max_length=10, null=True),
                ),
                ("subtotal", models.CharField(blank=True, max_length=10, null=True)),
                (
                    "payment_mode",
                    models.CharField(
                        choices=[
                            ("Cash", "Cash"),
                            ("Transfer to Bank A/C", "Transfer to Bank A/C"),
                            ("UPI", "UPI"),
                            ("Card", "Card"),
                            ("Insurance", "Insurance"),
                        ],
                        default="Cash",
                        max_length=50,
                    ),
                ),
                ("net_amount", models.CharField(blank=True, max_length=50, null=True)),
                ("paid_amount", models.CharField(blank=True, max_length=50, null=True)),
                ("due_amount", models.CharField(blank=True, max_length=50, null=True)),
                ("created_at", models.DateField(auto_now_add=True, null=True)),
                ("updated_at", models.DateField(auto_now=True, null=True)),
                (
                    "doctor",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="staff_management.employee",
                    ),
                ),
                (
                    "patient",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="patients.patient",
                    ),
                ),
                (
                    "tenant",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="users.tenant",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="IPD",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("height", models.CharField(blank=True, max_length=10, null=True)),
                ("bp", models.CharField(blank=True, max_length=10, null=True)),
                ("pulse", models.CharField(blank=True, max_length=10, null=True)),
                ("temperature", models.CharField(blank=True, max_length=10, null=True)),
                ("respiration", models.CharField(blank=True, max_length=10, null=True)),
                ("symptoms", models.TextField(blank=True, null=True)),
                ("previous_medical_issue", models.TextField(blank=True, null=True)),
                ("bed_no", models.CharField(blank=True, max_length=10, null=True)),
                ("ward", models.CharField(blank=True, max_length=10, null=True)),
                ("floor", models.CharField(blank=True, max_length=10, null=True)),
                (
                    "casualty",
                    models.CharField(
                        choices=[("No", "No"), ("Yes", "Yes")],
                        default="No",
                        max_length=5,
                    ),
                ),
                ("notes", models.TextField(blank=True, null=True)),
                ("created_at", models.DateField(auto_now_add=True, null=True)),
                ("updated_at", models.DateField(auto_now=True, null=True)),
                (
                    "doctor",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="staff_management.employee",
                    ),
                ),
                (
                    "patient",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="patients.patient",
                    ),
                ),
                (
                    "tenant",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="users.tenant",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]