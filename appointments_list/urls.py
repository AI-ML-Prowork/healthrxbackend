from django.urls import path
from .views import *



urlpatterns = [
    path("appointment", AppointmentListView.as_view(), name="appointment-list"),
    path("appointment/<int:bill_id>", AppointmentManagementView.as_view(), name="appointment-manage"),
]
