from django.urls import path
from .views import *

urlpatterns = [
    path("pathology", PathologyListView.as_view(), name="pathology-list"),
    path("pathology/<int:opd_id>", PathologyManagementView.as_view(), name="pathology-manage"),
    path("pathology-bill", PathologyBillListView.as_view(), name="pathology-bill-list"),
    path("pathology-bill/<int:opd_bill_id>", PathologyBillManagementView.as_view(), name="pathology-bill-manage"),
]
