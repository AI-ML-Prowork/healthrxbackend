from django.db import IntegrityError
from elevenlabs import ValidationError
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from .models import IPD,IPDBill
from rest_framework.permissions import IsAuthenticated
from clients.custom_permissions import IsTenantAdminOrIsUserPartOfTenant
import logging

logger = logging.getLogger(__name__)

class IPDListView(APIView):
    # permission_classes = [IsAuthenticated, IsTenantAdminOrIsUserPartOfTenant]

    # GET: List all ipd for the tenant
    def get(self, request):
        patient_id = request.query_params.get("patient")  # Get 'patient' query parameter from URL
        if patient_id:
            # Filter ipd with the specific patient ID
            ipd = IPD.objects.filter(tenant=request.tenant, patient__id=patient_id)
        else:
            # Fetch all ipd if no 'patient' parameter is provided
            ipd = IPD.objects.filter(tenant=request.tenant)
        
        serializer = IPDSerializer(ipd, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    # POST: Add a new IPD
    def post(self, request):
        serializer = IPDCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Save IPD with user and tenant
                serializer.save(user=request.user, tenant=request.tenant)
                return Response({"msg": "IPD added successfully!"}, status=status.HTTP_201_CREATED)
            except IntegrityError as e:
                raise ValidationError({"error": str(e)})
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class IPDManagementView(APIView):
    permission_classes = [IsAuthenticated, IsTenantAdminOrIsUserPartOfTenant]

    def get(self, request, ipd_id):
        try:
            ipd = IPD.objects.get(id=ipd_id, tenant=request.tenant)
            serializer = IPDSerializer(ipd)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        except IPD.DoesNotExist:
            return Response({"msg": "IPD not found."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = IPDCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(tenant=request.tenant)
            return Response({"msg": "IPD added successfully!"}, status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, ipd_id):
        try:
            ipd = IPD.objects.get(id=ipd_id, tenant=request.tenant)
            serializer = IPDCreateUpdateSerializer(ipd, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"msg": "IPD updated successfully!"}, status=status.HTTP_200_OK)
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except IPD.DoesNotExist:
            return Response({"msg": "IPD not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, ipd_id):
        try:
            ipd = IPD.objects.get(id=ipd_id, tenant=request.tenant)
            ipd.delete()
            return Response({"msg": "IPD deleted successfully!"}, status=status.HTTP_200_OK)
        except IPD.DoesNotExist:
            return Response({"msg": "IPD not found."}, status=status.HTTP_404_NOT_FOUND)

    permission_classes = [IsAuthenticated, IsTenantAdminOrIsUserPartOfTenant]

   
    def get(self, request, ipd_id):
        try:
            # Tenant admin can access all ipd, while users can only access their own ipd
            if request.user.is_tenant_admin:
                ipd = IPD.objects.get(id=ipd_id)
            else:
                ipd = IPD.objects.get(id=ipd_id, user=request.user)
        except IPD.DoesNotExist as e:
            logger.critical(f"Error fetching ipd: {e}")
            return Response(
                {"msg": f"IPD with ID {ipd_id} not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = IPDSerializer(ipd)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    # PATCH: Update specific ipd details
    def patch(self, request, ipd_id):
        try:
            if request.user.is_tenant_admin:
                ipd = IPD.objects.get(id=ipd_id)
            else:
                ipd = IPD.objects.get(id=ipd_id, user=request.user)
        except IPD.DoesNotExist as e:
            logger.critical(f"Error fetching ipd for update: {e}")
            return Response(
                {"msg": f"IPD with ID {ipd_id} not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = IPDSerializer(ipd, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user, tenant=request.tenant)
            return Response({"msg": "IPD updated successfully!"}, status=status.HTTP_200_OK)
        logger.error(f"Error while updating ipd: {serializer.errors}")
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )

    # DELETE: Delete specific ipd
    def delete(self, request, ipd_id):
        try:
            if request.user.is_tenant_admin:
                ipd = IPD.objects.get(id=ipd_id)
            else:
                ipd = IPD.objects.get(id=ipd_id, user=request.user)
        except IPD.DoesNotExist as e:
            logger.critical(f"Error deleting ipd: {e}")
            return Response(
                {"msg": f"IPD with ID {ipd_id} not found or already deleted."},
                status=status.HTTP_404_NOT_FOUND,
            )

        ipd.delete()
        logger.info("IPD deleted successfully!")
        return Response({"msg": "IPD deleted successfully!"}, status=status.HTTP_200_OK)
   
    
class IPDBillListView(APIView):
    # permission_classes = [IsAuthenticated, IsTenantAdminOrIsUserPartOfTenant]

    # GET: List all ipd for the tenant
    def get(self, request):
        patient_id = request.query_params.get("patient")  # Get 'patient' query parameter from URL
        if patient_id:
            # Filter ipd bill with the specific patient ID
            ipd = IPDBill.objects.filter(tenant=request.tenant, patient__id=patient_id)
        else:
            # Fetch all ipd bill if no 'patient' parameter is provided
            ipd = IPDBill.objects.filter(tenant=request.tenant)
        
        serializer = IPDBillSerializer(ipd, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    # POST: Add a new IPD Bill
    def post(self, request):
        serializer = IPDBillCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Save IPD Bill with user and tenant
                serializer.save(user=request.user, tenant=request.tenant)
                return Response({"msg": "IPD Bill added successfully!"}, status=status.HTTP_201_CREATED)
            except IntegrityError as e:
                raise ValidationError({"error": str(e)})
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class IPDBillManagementView(APIView):
    permission_classes = [IsAuthenticated, IsTenantAdminOrIsUserPartOfTenant]

    def get(self, request, ipd_bill_id):
        try:
            ipd = IPDBill.objects.get(id=ipd_bill_id, tenant=request.tenant)
            serializer = IPDBillSerializer(ipd)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        except IPDBill.DoesNotExist:
            return Response({"msg": "IPD Bill not found."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = IPDBillCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(tenant=request.tenant)
            return Response({"msg": "IPD Bill added successfully!"}, status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, ipd_bill_id):
        try:
            ipd = IPDBill.objects.get(id=ipd_bill_id, tenant=request.tenant)
            serializer = IPDBillCreateUpdateSerializer(ipd, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"msg": "IPD Bill updated successfully!"}, status=status.HTTP_200_OK)
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except IPDBill.DoesNotExist:
            return Response({"msg": "IPD Bill not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, ipd_bill_id):
        try:
            ipd = IPDBill.objects.get(id=ipd_bill_id, tenant=request.tenant)
            ipd.delete()
            return Response({"msg": "IPD Bill deleted successfully!"}, status=status.HTTP_200_OK)
        except IPDBill.DoesNotExist:
            return Response({"msg": "IPD Bill not found."}, status=status.HTTP_404_NOT_FOUND)

    permission_classes = [IsAuthenticated, IsTenantAdminOrIsUserPartOfTenant]

   
    def get(self, request, ipd_bill_id):
        try:
            # Tenant admin can access all ipd, while users can only access their own ipd
            if request.user.is_tenant_admin:
                ipd = IPDBill.objects.get(id=ipd_bill_id)
            else:
                ipd = IPDBill.objects.get(id=ipd_bill_id, user=request.user)
        except IPDBill.DoesNotExist as e:
            logger.critical(f"Error fetching ipd bill: {e}")
            return Response(
                {"msg": f"IPD Bill with ID {ipd_bill_id} not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = IPDBillSerializer(ipd)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    # PATCH: Update specific ipd details
    def patch(self, request, ipd_bill_id):
        try:
            if request.user.is_tenant_admin:
                ipd = IPDBill.objects.get(id=ipd_bill_id)
            else:
                ipd = IPDBill.objects.get(id=ipd_bill_id, user=request.user)
        except IPDBill.DoesNotExist as e:
            logger.critical(f"Error fetching ipd bill for update: {e}")
            return Response(
                {"msg": f"IPD Bill with ID {ipd_bill_id} not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = IPDBillSerializer(ipd, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user, tenant=request.tenant)
            return Response({"msg": "IPD Bill updated successfully!"}, status=status.HTTP_200_OK)
        logger.error(f"Error while updating ipd bill: {serializer.errors}")
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )

    # DELETE: Delete specific ipd
    def delete(self, request, ipd_bill_id):
        try:
            if request.user.is_tenant_admin:
                ipd = IPDBill.objects.get(id=ipd_bill_id)
            else:
                ipd = IPDBill.objects.get(id=ipd_bill_id, user=request.user)
        except IPDBill.DoesNotExist as e:
            logger.critical(f"Error deleting ipd bill: {e}")
            return Response(
                {"msg": f"IPD Bill with ID {ipd_bill_id} not found or already deleted."},
                status=status.HTTP_404_NOT_FOUND,
            )

        ipd.delete()
        logger.info("IPD Bill deleted successfully!")
        return Response({"msg": "IPD Bill deleted successfully!"}, status=status.HTTP_200_OK)
