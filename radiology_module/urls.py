from django.urls import path
from .views import *

urlpatterns = [
    path("radiology", RadiologyListView.as_view(), name="radiology-list"),
    path("radiology/<int:radiology_id>", RadiologyManagementView.as_view(), name="radiology-manage"),
    path("radiology-bill", RadiologyBillListView.as_view(), name="radiology-bill-list"),
    path("radiology-bill/<int:radiology_bill_id>", RadiologyBillManagementView.as_view(), name="radiology-bill-manage"),
]
