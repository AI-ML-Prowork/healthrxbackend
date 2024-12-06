from django.db import IntegrityError
from elevenlabs import ValidationError
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from .models import Billing
from rest_framework.permissions import IsAuthenticated
from clients.custom_permissions import IsTenantAdminOrIsUserPartOfTenant
import logging

logger = logging.getLogger(__name__)

class BillingListView(APIView):
    # permission_classes = [IsAuthenticated, IsTenantAdminOrIsUserPartOfTenant]

    # GET: List all billings for the tenant
    def get(self, request):
        patient_id = request.query_params.get("patient")  # Get 'patient' query parameter from URL
        if patient_id:
            # Filter billings with the specific patient ID
            billings = Billing.objects.filter(tenant=request.tenant, patient__id=patient_id)
        else:
            # Fetch all billings if no 'patient' parameter is provided
            billings = Billing.objects.filter(tenant=request.tenant)
        
        serializer = BillingSerializer(billings, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    # POST: Add a new billing
    def post(self, request):
        serializer = BillingCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Save billing with user and tenant
                serializer.save(user=request.user, tenant=request.tenant)
                return Response({"msg": "Billing added successfully!"}, status=status.HTTP_201_CREATED)
            except IntegrityError as e:
                raise ValidationError({"error": str(e)})
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class BillingManagementView(APIView):
    permission_classes = [IsAuthenticated, IsTenantAdminOrIsUserPartOfTenant]

    def get(self, request, bill_id):
        try:
            billing = Billing.objects.get(id=bill_id, tenant=request.tenant)
            serializer = BillingSerializer(billing)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        except Billing.DoesNotExist:
            return Response({"msg": "Billing not found."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = BillingCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(tenant=request.tenant)
            return Response({"msg": "Billing added successfully!"}, status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, bill_id):
        try:
            billing = Billing.objects.get(id=bill_id, tenant=request.tenant)
            serializer = BillingCreateUpdateSerializer(billing, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"msg": "Billing updated successfully!"}, status=status.HTTP_200_OK)
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Billing.DoesNotExist:
            return Response({"msg": "Billing not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, bill_id):
        try:
            billing = Billing.objects.get(id=bill_id, tenant=request.tenant)
            billing.delete()
            return Response({"msg": "Billing deleted successfully!"}, status=status.HTTP_200_OK)
        except Billing.DoesNotExist:
            return Response({"msg": "Billing not found."}, status=status.HTTP_404_NOT_FOUND)

    permission_classes = [IsAuthenticated, IsTenantAdminOrIsUserPartOfTenant]

   
    def get(self, request, bill_id):
        try:
            # Tenant admin can access all billings, while users can only access their own billings
            if request.user.is_tenant_admin:
                billing = Billing.objects.get(id=bill_id)
            else:
                billing = Billing.objects.get(id=bill_id, user=request.user)
        except Billing.DoesNotExist as e:
            logger.critical(f"Error fetching billing: {e}")
            return Response(
                {"msg": f"Billing with ID {bill_id} not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = BillingSerializer(billing)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    # PATCH: Update specific billing details
    def patch(self, request, bill_id):
        try:
            if request.user.is_tenant_admin:
                billing = Billing.objects.get(id=bill_id)
            else:
                billing = Billing.objects.get(id=bill_id, user=request.user)
        except Billing.DoesNotExist as e:
            logger.critical(f"Error fetching billing for update: {e}")
            return Response(
                {"msg": f"Billing with ID {bill_id} not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = BillingSerializer(billing, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user, tenant=request.tenant)
            return Response({"msg": "Billing updated successfully!"}, status=status.HTTP_200_OK)
        logger.error(f"Error while updating billing: {serializer.errors}")
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )

    # DELETE: Delete specific billing
    def delete(self, request, bill_id):
        try:
            if request.user.is_tenant_admin:
                billing = Billing.objects.get(id=bill_id)
            else:
                billing = Billing.objects.get(id=bill_id, user=request.user)
        except Billing.DoesNotExist as e:
            logger.critical(f"Error deleting billing: {e}")
            return Response(
                {"msg": f"Billing with ID {bill_id} not found or already deleted."},
                status=status.HTTP_404_NOT_FOUND,
            )

        billing.delete()
        logger.info("Billing deleted successfully!")
        return Response({"msg": "Billing deleted successfully!"}, status=status.HTTP_200_OK)