from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from .models import Patient
from rest_framework.permissions import IsAuthenticated
from clients.custom_permissions import IsTenantAdminOrIsUserPartOfTenant
import logging

logger = logging.getLogger(__name__)

class PatientView(APIView):
    permission_classes = [IsAuthenticated, IsTenantAdminOrIsUserPartOfTenant]

    # POST: Create a new patient
    def post(self, request):
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            patient = serializer.save(user=request.user, tenant=request.tenant)
            logger.info("Patient added successfully!")
            return Response(
                {"msg": "Patient added successfully!", "patient_id": patient.id},
                status=status.HTTP_201_CREATED,
            )
        logger.error(f"Error while creating patient: {serializer.errors}")
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )

    # GET: List patients for the authenticated user
    def get(self, request):
        logger.info("Fetching patients for the authenticated user and tenant.")
        patients = Patient.objects.filter(user=request.user)
        serializer = PatientSerializer(patients, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)



class FetchAllPatients(APIView):
    permission_classes = [IsAuthenticated, IsTenantAdminOrIsUserPartOfTenant]

    def get(self, request):
        logger.info("Fetching all patients within the same tenant.")
        patients = Patient.objects.all()
        serializer = PatientSerializer(patients, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)





from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class PatientManagementView(APIView):
    permission_classes = [IsAuthenticated, IsTenantAdminOrIsUserPartOfTenant]

    # GET: Fetch specific patient details
    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter(
            "patient_id", openapi.IN_PATH, description="Patient ID", type=openapi.TYPE_INTEGER)]
    )
    def get(self, request, patient_id):
        try:
            # Tenant admin can access all patients, while users can only access their own patients
            if request.user.is_tenant_admin:
                patient = Patient.objects.get(id=patient_id)
            else:
                patient = Patient.objects.get(id=patient_id, user=request.user)
        except Patient.DoesNotExist as e:
            logger.critical(f"Error fetching patient: {e}")
            return Response(
                {"msg": f"Patient with ID {patient_id} not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = PatientSerializer(patient)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    # PATCH: Update specific patient details
    def patch(self, request, patient_id):
        try:
            if request.user.is_tenant_admin:
                patient = Patient.objects.get(id=patient_id)
            else:
                patient = Patient.objects.get(id=patient_id, user=request.user)
        except Patient.DoesNotExist as e:
            logger.critical(f"Error fetching patient for update: {e}")
            return Response(
                {"msg": f"Patient with ID {patient_id} not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = PatientSerializer(patient, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user, tenant=request.tenant)
            return Response({"msg": "Patient updated successfully!"}, status=status.HTTP_200_OK)
        logger.error(f"Error while updating patient: {serializer.errors}")
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )

    # DELETE: Delete specific patient
    def delete(self, request, patient_id):
        try:
            if request.user.is_tenant_admin:
                patient = Patient.objects.get(id=patient_id)
            else:
                patient = Patient.objects.get(id=patient_id, user=request.user)
        except Patient.DoesNotExist as e:
            logger.critical(f"Error deleting patient: {e}")
            return Response(
                {"msg": f"Patient with ID {patient_id} not found or already deleted."},
                status=status.HTTP_404_NOT_FOUND,
            )

        patient.delete()
        logger.info("Patient deleted successfully!")
        return Response({"msg": "Patient deleted successfully!"}, status=status.HTTP_200_OK)