"""
URL configuration for saas_admin project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from django.urls import include
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


urlpatterns = [
    path("", include("clients.urls")),
    path("api/", include("notifications.urls")),
    path("search/", include("search.urls")),

    # new urls by today only...
    path('api/patients/', include('patients.urls')),
    path('api/appointments/', include('appointments_list.urls')),
    path('api/ambulance/', include('ambulance.urls')),
    path('api/ipd/', include('ipd_module.urls')),
    path('api/pathology/', include('pathology_module.urls')),
    path('api/staff/', include('staff_management.urls')),
    path('api/billing/', include('billing_counter.urls')),
    path('api/bed-management/', include('bed_management.urls')),
    path('api/blood-bank/', include('blood_bank.urls')),
    path('api/certificate/', include('certificate_module.urls')),
    path('api/dashboard/', include('dashboard.urls')),
    path('api/human-resource/', include('human_resource.urls')),
    path('api/leave-management/', include('leave_management.urls')),
    path('api/ops/', include('opd_module.urls')),
    path('api/pharmacy/', include('pharmacy_module.urls')),
    path('api/radiology/', include('radiology_module.urls')),
    path('api/tpa-insurance/', include('tpa_insurance.urls')),
    path('api/visitor-book/', include('visitor_book.urls')),
]


# urlpatterns += [
#     path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
# ]


