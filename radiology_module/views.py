from django.db import IntegrityError
from elevenlabs import ValidationError
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from .models import Radiology,RadiologyBill
from rest_framework.permissions import IsAuthenticated
from clients.custom_permissions import IsTenantAdminOrIsUserPartOfTenant
import logging

logger = logging.getLogger(__name__)

class RadiologyListView(APIView):
    # permission_classes = [IsAuthenticated, IsTenantAdminOrIsUserPartOfTenant]

    # GET: List all radiology for the tenant
    def get(self, request):
        patient_id = request.query_params.get("patient")  # Get 'patient' query parameter from URL
        if patient_id:
            # Filter radiology with the specific patient ID
            radiology = Radiology.objects.filter(tenant=request.tenant, patient__id=patient_id)
        else:
            # Fetch all radiology if no 'patient' parameter is provided
            radiology = Radiology.objects.filter(tenant=request.tenant)
        
        serializer = RadiologySerializer(radiology, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    # POST: Add a new Radiology
    def post(self, request):
        serializer = RadiologyCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Save Radiology with user and tenant
                serializer.save(user=request.user, tenant=request.tenant)
                return Response({"msg": "Radiology added successfully!"}, status=status.HTTP_201_CREATED)
            except IntegrityError as e:
                raise ValidationError({"error": str(e)})
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class RadiologyManagementView(APIView):
    permission_classes = [IsAuthenticated, IsTenantAdminOrIsUserPartOfTenant]

    def get(self, request, radiology_id):
        try:
            radiology = Radiology.objects.get(id=radiology_id, tenant=request.tenant)
            serializer = RadiologySerializer(radiology)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        except Radiology.DoesNotExist:
            return Response({"msg": "Radiology not found."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = RadiologyCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(tenant=request.tenant)
            return Response({"msg": "Radiology added successfully!"}, status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, radiology_id):
        try:
            radiology = Radiology.objects.get(id=radiology_id, tenant=request.tenant)
            serializer = RadiologyCreateUpdateSerializer(radiology, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"msg": "Radiology updated successfully!"}, status=status.HTTP_200_OK)
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Radiology.DoesNotExist:
            return Response({"msg": "Radiology not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, radiology_id):
        try:
            radiology = Radiology.objects.get(id=radiology_id, tenant=request.tenant)
            radiology.delete()
            return Response({"msg": "Radiology deleted successfully!"}, status=status.HTTP_200_OK)
        except Radiology.DoesNotExist:
            return Response({"msg": "Radiology not found."}, status=status.HTTP_404_NOT_FOUND)

    permission_classes = [IsAuthenticated, IsTenantAdminOrIsUserPartOfTenant]

   
    def get(self, request, radiology_id):
        try:
            # Tenant admin can access all radiology, while users can only access their own radiology
            if request.user.is_tenant_admin:
                radiology = Radiology.objects.get(id=radiology_id)
            else:
                radiology = Radiology.objects.get(id=radiology_id, user=request.user)
        except Radiology.DoesNotExist as e:
            logger.critical(f"Error fetching radiology: {e}")
            return Response(
                {"msg": f"Radiology with ID {radiology_id} not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = RadiologySerializer(radiology)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    # PATCH: Update specific radiology details
    def patch(self, request, radiology_id):
        try:
            if request.user.is_tenant_admin:
                radiology = Radiology.objects.get(id=radiology_id)
            else:
                radiology = Radiology.objects.get(id=radiology_id, user=request.user)
        except Radiology.DoesNotExist as e:
            logger.critical(f"Error fetching radiology for update: {e}")
            return Response(
                {"msg": f"Radiology with ID {radiology_id} not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = RadiologySerializer(radiology, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user, tenant=request.tenant)
            return Response({"msg": "Radiology updated successfully!"}, status=status.HTTP_200_OK)
        logger.error(f"Error while updating radiology: {serializer.errors}")
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )

    # DELETE: Delete specific radiology
    def delete(self, request, radiology_id):
        try:
            if request.user.is_tenant_admin:
                radiology = Radiology.objects.get(id=radiology_id)
            else:
                radiology = Radiology.objects.get(id=radiology_id, user=request.user)
        except Radiology.DoesNotExist as e:
            logger.critical(f"Error deleting radiology: {e}")
            return Response(
                {"msg": f"Radiology with ID {radiology_id} not found or already deleted."},
                status=status.HTTP_404_NOT_FOUND,
            )

        radiology.delete()
        logger.info("Radiology deleted successfully!")
        return Response({"msg": "Radiology deleted successfully!"}, status=status.HTTP_200_OK)
   
    
class RadiologyBillListView(APIView):
    # permission_classes = [IsAuthenticated, IsTenantAdminOrIsUserPartOfTenant]

    # GET: List all radiology for the tenant
    def get(self, request):
        patient_id = request.query_params.get("patient")  # Get 'patient' query parameter from URL
        if patient_id:
            # Filter radiology bill with the specific patient ID
            radiology = RadiologyBill.objects.filter(tenant=request.tenant, patient__id=patient_id)
        else:
            # Fetch all radiology bill if no 'patient' parameter is provided
            radiology = RadiologyBill.objects.filter(tenant=request.tenant)
        
        serializer = RadiologyBillSerializer(radiology, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    # POST: Add a new Radiology Bill
    def post(self, request):
        serializer = RadiologyBillCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Save Radiology Bill with user and tenant
                serializer.save(user=request.user, tenant=request.tenant)
                return Response({"msg": "Radiology Bill added successfully!"}, status=status.HTTP_201_CREATED)
            except IntegrityError as e:
                raise ValidationError({"error": str(e)})
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class RadiologyBillManagementView(APIView):
    permission_classes = [IsAuthenticated, IsTenantAdminOrIsUserPartOfTenant]

    def get(self, request, radiology_bill_id):
        try:
            radiology = RadiologyBill.objects.get(id=radiology_bill_id, tenant=request.tenant)
            serializer = RadiologyBillSerializer(radiology)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        except RadiologyBill.DoesNotExist:
            return Response({"msg": "Radiology Bill not found."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = RadiologyBillCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(tenant=request.tenant)
            return Response({"msg": "Radiology Bill added successfully!"}, status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, radiology_bill_id):
        try:
            radiology = RadiologyBill.objects.get(id=radiology_bill_id, tenant=request.tenant)
            serializer = RadiologyBillCreateUpdateSerializer(radiology, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"msg": "Radiology Bill updated successfully!"}, status=status.HTTP_200_OK)
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except RadiologyBill.DoesNotExist:
            return Response({"msg": "Radiology Bill not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, radiology_bill_id):
        try:
            radiology = RadiologyBill.objects.get(id=radiology_bill_id, tenant=request.tenant)
            radiology.delete()
            return Response({"msg": "Radiology Bill deleted successfully!"}, status=status.HTTP_200_OK)
        except RadiologyBill.DoesNotExist:
            return Response({"msg": "Radiology Bill not found."}, status=status.HTTP_404_NOT_FOUND)

    permission_classes = [IsAuthenticated, IsTenantAdminOrIsUserPartOfTenant]

   
    def get(self, request, radiology_bill_id):
        try:
            # Tenant admin can access all radiology, while users can only access their own radiology
            if request.user.is_tenant_admin:
                radiology = RadiologyBill.objects.get(id=radiology_bill_id)
            else:
                radiology = RadiologyBill.objects.get(id=radiology_bill_id, user=request.user)
        except RadiologyBill.DoesNotExist as e:
            logger.critical(f"Error fetching radiology bill: {e}")
            return Response(
                {"msg": f"Radiology Bill with ID {radiology_bill_id} not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = RadiologyBillSerializer(radiology)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    # PATCH: Update specific radiology details
    def patch(self, request, radiology_bill_id):
        try:
            if request.user.is_tenant_admin:
                radiology = RadiologyBill.objects.get(id=radiology_bill_id)
            else:
                radiology = RadiologyBill.objects.get(id=radiology_bill_id, user=request.user)
        except RadiologyBill.DoesNotExist as e:
            logger.critical(f"Error fetching radiology bill for update: {e}")
            return Response(
                {"msg": f"Radiology Bill with ID {radiology_bill_id} not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = RadiologyBillSerializer(radiology, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user, tenant=request.tenant)
            return Response({"msg": "Radiology Bill updated successfully!"}, status=status.HTTP_200_OK)
        logger.error(f"Error while updating radiology bill: {serializer.errors}")
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )

    # DELETE: Delete specific radiology
    def delete(self, request, radiology_bill_id):
        try:
            if request.user.is_tenant_admin:
                radiology = RadiologyBill.objects.get(id=radiology_bill_id)
            else:
                radiology = RadiologyBill.objects.get(id=radiology_bill_id, user=request.user)
        except RadiologyBill.DoesNotExist as e:
            logger.critical(f"Error deleting radiology bill: {e}")
            return Response(
                {"msg": f"Radiology Bill with ID {radiology_bill_id} not found or already deleted."},
                status=status.HTTP_404_NOT_FOUND,
            )

        radiology.delete()
        logger.info("Radiology Bill deleted successfully!")
        return Response({"msg": "Radiology Bill deleted successfully!"}, status=status.HTTP_200_OK)
