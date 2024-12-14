from django.urls import path
from .views import *

urlpatterns = [
    path("pathology", PathologyListView.as_view(), name="pathology-list"),
    path("pathology/<int:pathology_id>", PathologyManagementView.as_view(), name="pathology-manage"),
    path("pathology-bill", PathologyBillListView.as_view(), name="pathology-bill-list"),
    path("pathology-bill/<int:pathology_bill_id>", PathologyBillManagementView.as_view(), name="pathology-bill-manage"),
]
