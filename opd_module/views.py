from django.db import IntegrityError
from elevenlabs import ValidationError
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from .models import OPD
from rest_framework.permissions import IsAuthenticated
from clients.custom_permissions import IsTenantAdminOrIsUserPartOfTenant
import logging

logger = logging.getLogger(__name__)

class OPDListView(APIView):
    # permission_classes = [IsAuthenticated, IsTenantAdminOrIsUserPartOfTenant]

    # GET: List all opd for the tenant
    def get(self, request):
        patient_id = request.query_params.get("patient")  # Get 'patient' query parameter from URL
        if patient_id:
            # Filter opd with the specific patient ID
            opd = OPD.objects.filter(tenant=request.tenant, patient__id=patient_id)
        else:
            # Fetch all opd if no 'patient' parameter is provided
            opd = OPD.objects.filter(tenant=request.tenant)
        
        serializer = OPDSerializer(opd, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    # POST: Add a new OPD
    def post(self, request):
        serializer = OPDCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Save OPD with user and tenant
                serializer.save(user=request.user, tenant=request.tenant)
                return Response({"msg": "OPD added successfully!"}, status=status.HTTP_201_CREATED)
            except IntegrityError as e:
                raise ValidationError({"error": str(e)})
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class OPDManagementView(APIView):
    permission_classes = [IsAuthenticated, IsTenantAdminOrIsUserPartOfTenant]

    def get(self, request, opd_id):
        try:
            opd = OPD.objects.get(id=opd_id, tenant=request.tenant)
            serializer = OPDSerializer(opd)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        except OPD.DoesNotExist:
            return Response({"msg": "OPD not found."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = OPDCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(tenant=request.tenant)
            return Response({"msg": "OPD added successfully!"}, status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, opd_id):
        try:
            opd = OPD.objects.get(id=opd_id, tenant=request.tenant)
            serializer = OPDCreateUpdateSerializer(opd, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"msg": "OPD updated successfully!"}, status=status.HTTP_200_OK)
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except OPD.DoesNotExist:
            return Response({"msg": "OPD not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, opd_id):
        try:
            opd = OPD.objects.get(id=opd_id, tenant=request.tenant)
            opd.delete()
            return Response({"msg": "OPD deleted successfully!"}, status=status.HTTP_200_OK)
        except OPD.DoesNotExist:
            return Response({"msg": "OPD not found."}, status=status.HTTP_404_NOT_FOUND)

    permission_classes = [IsAuthenticated, IsTenantAdminOrIsUserPartOfTenant]

   
    def get(self, request, opd_id):
        try:
            # Tenant admin can access all opd, while users can only access their own opd
            if request.user.is_tenant_admin:
                opd = OPD.objects.get(id=opd_id)
            else:
                opd = OPD.objects.get(id=opd_id, user=request.user)
        except OPD.DoesNotExist as e:
            logger.critical(f"Error fetching opd: {e}")
            return Response(
                {"msg": f"OPD with ID {opd_id} not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = OPDSerializer(opd)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    # PATCH: Update specific opd details
    def patch(self, request, opd_id):
        try:
            if request.user.is_tenant_admin:
                opd = OPD.objects.get(id=opd_id)
            else:
                opd = OPD.objects.get(id=opd_id, user=request.user)
        except OPD.DoesNotExist as e:
            logger.critical(f"Error fetching opd for update: {e}")
            return Response(
                {"msg": f"OPD with ID {opd_id} not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = OPDSerializer(opd, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user, tenant=request.tenant)
            return Response({"msg": "OPD updated successfully!"}, status=status.HTTP_200_OK)
        logger.error(f"Error while updating opd: {serializer.errors}")
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )

    # DELETE: Delete specific opd
    def delete(self, request, opd_id):
        try:
            if request.user.is_tenant_admin:
                opd = OPD.objects.get(id=opd_id)
            else:
                opd = OPD.objects.get(id=opd_id, user=request.user)
        except OPD.DoesNotExist as e:
            logger.critical(f"Error deleting opd: {e}")
            return Response(
                {"msg": f"OPD with ID {opd_id} not found or already deleted."},
                status=status.HTTP_404_NOT_FOUND,
            )

        opd.delete()
        logger.info("OPD deleted successfully!")
        return Response({"msg": "OPD deleted successfully!"}, status=status.HTTP_200_OK)