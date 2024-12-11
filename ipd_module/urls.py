from django.urls import path
from .views import *

urlpatterns = [
    path("ipd", IPDListView.as_view(), name="ipd-list"),
    path("ipd/<int:opd_id>", IPDManagementView.as_view(), name="ipd-manage"),
    path("ipd-bill", IPDBillListView.as_view(), name="ipd-bill-list"),
    path("ipd-bill/<int:opd_bill_id>", IPDBillManagementView.as_view(), name="ipd-bill-manage"),
]
