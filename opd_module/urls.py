from django.urls import path
from .views import *

urlpatterns = [
    path("opd", OPDListView.as_view(), name="opd-list"),
    path("opd/<int:opd_id>", OPDManagementView.as_view(), name="opd-manage"),
]
