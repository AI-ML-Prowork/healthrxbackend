from django.urls import path
from .views import *



urlpatterns = [
    path("billing", BillingListView.as_view(), name="billing-list"),
    path("billing/<int:bill_id>", BillingManagementView.as_view(), name="billing-manage"),
]
