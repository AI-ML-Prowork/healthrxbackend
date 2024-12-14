from django.urls import path
from .views import *

urlpatterns = [
    path("medicine", MedicineListView.as_view(), name="medicine-list"),
    path("medicine/<int:medicine_id>", MedicineManagementView.as_view(), name="medicine-manage"),
    path("pharmacy-bill", PharmacyBillListView.as_view(), name="pharmacy-bill-list"),
    path("pharmacy-bill/<int:pharmacy_bill_id>", PharmacyBillManagementView.as_view(), name="pharmacy-bill-manage"),
    path("purchase-medicine", PurchaseMedicineView.as_view(), name="medicine-list"),
    path("purchase-medicine/<int:purchase_medicine_id>", PurchaseMedicineManagementView.as_view(), name="medicine-manage"),
]
