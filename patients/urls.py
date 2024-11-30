from django.urls import path
from .views import *


urlpatterns = [
    path("patient", PatientView.as_view(), name="patients-list"),
    path("patient/<int:patient_id>", PatientManagementView.as_view(), name="patient-manage"),
    path("all-patient", FetchAllPatients.as_view(), name="get-all-patients"),
]