from django.db import IntegrityError
from elevenlabs import ValidationError
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from .models import Appointment
from rest_framework.permissions import IsAuthenticated
from clients.custom_permissions import IsTenantAdminOrIsUserPartOfTenant
import logging

logger = logging.getLogger(__name__)

class AppointmentListView(APIView):
    # permission_classes = [IsAuthenticated, IsTenantAdminOrIsUserPartOfTenant]

    # GET: List all appointments for the tenant
    def get(self, request):
        patient_id = request.query_params.get("patient")  # Get 'patient' query parameter from URL
        if patient_id:
            # Filter appointments with the specific patient ID
            appointments = Appointment.objects.filter(tenant=request.tenant, patient__id=patient_id)
        else:
            # Fetch all appointments if no 'patient' parameter is provided
            appointments = Appointment.objects.filter(tenant=request.tenant)
        
        serializer = AppointmentSerializer(appointments, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    # POST: Add a new appointment
    def post(self, request):
        serializer = AppointmentCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Save appointment with user and tenant
                serializer.save(user=request.user, tenant=request.tenant)
                return Response({"msg": "Appointment added successfully!"}, status=status.HTTP_201_CREATED)
            except IntegrityError as e:
                raise ValidationError({"error": str(e)})
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class AppointmentManagementView(APIView):
    permission_classes = [IsAuthenticated, IsTenantAdminOrIsUserPartOfTenant]

    def get(self, request, appointment_id):
        try:
            appointment = Appointment.objects.get(id=appointment_id, tenant=request.tenant)
            serializer = AppointmentSerializer(appointment)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        except Appointment.DoesNotExist:
            return Response({"msg": "Appointment not found."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = AppointmentCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(tenant=request.tenant)
            return Response({"msg": "Appointment added successfully!"}, status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, appointment_id):
        try:
            appointment = Appointment.objects.get(id=appointment_id, tenant=request.tenant)
            serializer = AppointmentCreateUpdateSerializer(appointment, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"msg": "Appointment updated successfully!"}, status=status.HTTP_200_OK)
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Appointment.DoesNotExist:
            return Response({"msg": "Appointment not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, appointment_id):
        try:
            appointment = Appointment.objects.get(id=appointment_id, tenant=request.tenant)
            appointment.delete()
            return Response({"msg": "Appointment deleted successfully!"}, status=status.HTTP_200_OK)
        except Appointment.DoesNotExist:
            return Response({"msg": "Appointment not found."}, status=status.HTTP_404_NOT_FOUND)

    permission_classes = [IsAuthenticated, IsTenantAdminOrIsUserPartOfTenant]

   
    def get(self, request, appointment_id):
        try:
            # Tenant admin can access all appointments, while users can only access their own appointments
            if request.user.is_tenant_admin:
                appointment = Appointment.objects.get(id=appointment_id)
            else:
                appointment = Appointment.objects.get(id=appointment_id, user=request.user)
        except Appointment.DoesNotExist as e:
            logger.critical(f"Error fetching appointment: {e}")
            return Response(
                {"msg": f"Appointment with ID {appointment_id} not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = AppointmentSerializer(appointment)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    # PATCH: Update specific appointment details
    def patch(self, request, appointment_id):
        try:
            if request.user.is_tenant_admin:
                appointment = Appointment.objects.get(id=appointment_id)
            else:
                appointment = Appointment.objects.get(id=appointment_id, user=request.user)
        except Appointment.DoesNotExist as e:
            logger.critical(f"Error fetching appointment for update: {e}")
            return Response(
                {"msg": f"Appointment with ID {appointment_id} not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = AppointmentSerializer(appointment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user, tenant=request.tenant)
            return Response({"msg": "Appointment updated successfully!"}, status=status.HTTP_200_OK)
        logger.error(f"Error while updating appointment: {serializer.errors}")
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )

    # DELETE: Delete specific appointment
    def delete(self, request, appointment_id):
        try:
            if request.user.is_tenant_admin:
                appointment = Appointment.objects.get(id=appointment_id)
            else:
                appointment = Appointment.objects.get(id=appointment_id, user=request.user)
        except Appointment.DoesNotExist as e:
            logger.critical(f"Error deleting appointment: {e}")
            return Response(
                {"msg": f"Appointment with ID {appointment_id} not found or already deleted."},
                status=status.HTTP_404_NOT_FOUND,
            )

        appointment.delete()
        logger.info("Appointment deleted successfully!")
        return Response({"msg": "Appointment deleted successfully!"}, status=status.HTTP_200_OK)