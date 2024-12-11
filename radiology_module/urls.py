from django.urls import path
from .views import *

urlpatterns = [
    path("radiology", RadiologyListView.as_view(), name="radiology-list"),
    path("radiology/<int:opd_id>", RadiologyManagementView.as_view(), name="radiology-manage"),
    path("radiology-bill", RadiologyBillListView.as_view(), name="radiology-bill-list"),
    path("radiology-bill/<int:opd_bill_id>", RadiologyBillManagementView.as_view(), name="radiology-bill-manage"),
]
