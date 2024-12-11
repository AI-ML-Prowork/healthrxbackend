from django.db import IntegrityError
from elevenlabs import ValidationError
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from .models import Pathology,PathologyBill
from rest_framework.permissions import IsAuthenticated
from clients.custom_permissions import IsTenantAdminOrIsUserPartOfTenant
import logging

logger = logging.getLogger(__name__)

class PathologyListView(APIView):
    # permission_classes = [IsAuthenticated, IsTenantAdminOrIsUserPartOfTenant]

    # GET: List all pathology for the tenant
    def get(self, request):
        patient_id = request.query_params.get("patient")  # Get 'patient' query parameter from URL
        if patient_id:
            # Filter pathology with the specific patient ID
            pathology = Pathology.objects.filter(tenant=request.tenant, patient__id=patient_id)
        else:
            # Fetch all pathology if no 'patient' parameter is provided
            pathology = Pathology.objects.filter(tenant=request.tenant)
        
        serializer = PathologySerializer(pathology, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    # POST: Add a new Pathology
    def post(self, request):
        serializer = PathologyCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Save Pathology with user and tenant
                serializer.save(user=request.user, tenant=request.tenant)
                return Response({"msg": "Pathology added successfully!"}, status=status.HTTP_201_CREATED)
            except IntegrityError as e:
                raise ValidationError({"error": str(e)})
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class PathologyManagementView(APIView):
    permission_classes = [IsAuthenticated, IsTenantAdminOrIsUserPartOfTenant]

    def get(self, request, pathology_id):
        try:
            pathology = Pathology.objects.get(id=pathology_id, tenant=request.tenant)
            serializer = PathologySerializer(pathology)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        except Pathology.DoesNotExist:
            return Response({"msg": "Pathology not found."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = PathologyCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(tenant=request.tenant)
            return Response({"msg": "Pathology added successfully!"}, status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pathology_id):
        try:
            pathology = Pathology.objects.get(id=pathology_id, tenant=request.tenant)
            serializer = PathologyCreateUpdateSerializer(pathology, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"msg": "Pathology updated successfully!"}, status=status.HTTP_200_OK)
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Pathology.DoesNotExist:
            return Response({"msg": "Pathology not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pathology_id):
        try:
            pathology = Pathology.objects.get(id=pathology_id, tenant=request.tenant)
            pathology.delete()
            return Response({"msg": "Pathology deleted successfully!"}, status=status.HTTP_200_OK)
        except Pathology.DoesNotExist:
            return Response({"msg": "Pathology not found."}, status=status.HTTP_404_NOT_FOUND)

    permission_classes = [IsAuthenticated, IsTenantAdminOrIsUserPartOfTenant]

   
    def get(self, request, pathology_id):
        try:
            # Tenant admin can access all pathology, while users can only access their own pathology
            if request.user.is_tenant_admin:
                pathology = Pathology.objects.get(id=pathology_id)
            else:
                pathology = Pathology.objects.get(id=pathology_id, user=request.user)
        except Pathology.DoesNotExist as e:
            logger.critical(f"Error fetching pathology: {e}")
            return Response(
                {"msg": f"Pathology with ID {pathology_id} not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = PathologySerializer(pathology)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    # PATCH: Update specific pathology details
    def patch(self, request, pathology_id):
        try:
            if request.user.is_tenant_admin:
                pathology = Pathology.objects.get(id=pathology_id)
            else:
                pathology = Pathology.objects.get(id=pathology_id, user=request.user)
        except Pathology.DoesNotExist as e:
            logger.critical(f"Error fetching pathology for update: {e}")
            return Response(
                {"msg": f"Pathology with ID {pathology_id} not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = PathologySerializer(pathology, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user, tenant=request.tenant)
            return Response({"msg": "Pathology updated successfully!"}, status=status.HTTP_200_OK)
        logger.error(f"Error while updating pathology: {serializer.errors}")
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )

    # DELETE: Delete specific pathology
    def delete(self, request, pathology_id):
        try:
            if request.user.is_tenant_admin:
                pathology = Pathology.objects.get(id=pathology_id)
            else:
                pathology = Pathology.objects.get(id=pathology_id, user=request.user)
        except Pathology.DoesNotExist as e:
            logger.critical(f"Error deleting pathology: {e}")
            return Response(
                {"msg": f"Pathology with ID {pathology_id} not found or already deleted."},
                status=status.HTTP_404_NOT_FOUND,
            )

        pathology.delete()
        logger.info("Pathology deleted successfully!")
        return Response({"msg": "Pathology deleted successfully!"}, status=status.HTTP_200_OK)
   
    
class PathologyBillListView(APIView):
    # permission_classes = [IsAuthenticated, IsTenantAdminOrIsUserPartOfTenant]

    # GET: List all pathology for the tenant
    def get(self, request):
        patient_id = request.query_params.get("patient")  # Get 'patient' query parameter from URL
        if patient_id:
            # Filter pathology bill with the specific patient ID
            pathology = PathologyBill.objects.filter(tenant=request.tenant, patient__id=patient_id)
        else:
            # Fetch all pathology bill if no 'patient' parameter is provided
            pathology = PathologyBill.objects.filter(tenant=request.tenant)
        
        serializer = PathologyBillSerializer(pathology, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    # POST: Add a new Pathology Bill
    def post(self, request):
        serializer = PathologyBillCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Save Pathology Bill with user and tenant
                serializer.save(user=request.user, tenant=request.tenant)
                return Response({"msg": "Pathology Bill added successfully!"}, status=status.HTTP_201_CREATED)
            except IntegrityError as e:
                raise ValidationError({"error": str(e)})
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class PathologyBillManagementView(APIView):
    permission_classes = [IsAuthenticated, IsTenantAdminOrIsUserPartOfTenant]

    def get(self, request, pathology_bill_id):
        try:
            pathology = PathologyBill.objects.get(id=pathology_bill_id, tenant=request.tenant)
            serializer = PathologyBillSerializer(pathology)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        except PathologyBill.DoesNotExist:
            return Response({"msg": "Pathology Bill not found."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = PathologyBillCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(tenant=request.tenant)
            return Response({"msg": "Pathology Bill added successfully!"}, status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pathology_bill_id):
        try:
            pathology = PathologyBill.objects.get(id=pathology_bill_id, tenant=request.tenant)
            serializer = PathologyBillCreateUpdateSerializer(pathology, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"msg": "Pathology Bill updated successfully!"}, status=status.HTTP_200_OK)
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except PathologyBill.DoesNotExist:
            return Response({"msg": "Pathology Bill not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pathology_bill_id):
        try:
            pathology = PathologyBill.objects.get(id=pathology_bill_id, tenant=request.tenant)
            pathology.delete()
            return Response({"msg": "Pathology Bill deleted successfully!"}, status=status.HTTP_200_OK)
        except PathologyBill.DoesNotExist:
            return Response({"msg": "Pathology Bill not found."}, status=status.HTTP_404_NOT_FOUND)

    permission_classes = [IsAuthenticated, IsTenantAdminOrIsUserPartOfTenant]

   
    def get(self, request, pathology_bill_id):
        try:
            # Tenant admin can access all pathology, while users can only access their own pathology
            if request.user.is_tenant_admin:
                pathology = PathologyBill.objects.get(id=pathology_bill_id)
            else:
                pathology = PathologyBill.objects.get(id=pathology_bill_id, user=request.user)
        except PathologyBill.DoesNotExist as e:
            logger.critical(f"Error fetching pathology bill: {e}")
            return Response(
                {"msg": f"Pathology Bill with ID {pathology_bill_id} not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = PathologyBillSerializer(pathology)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    # PATCH: Update specific pathology details
    def patch(self, request, pathology_bill_id):
        try:
            if request.user.is_tenant_admin:
                pathology = PathologyBill.objects.get(id=pathology_bill_id)
            else:
                pathology = PathologyBill.objects.get(id=pathology_bill_id, user=request.user)
        except PathologyBill.DoesNotExist as e:
            logger.critical(f"Error fetching pathology bill for update: {e}")
            return Response(
                {"msg": f"Pathology Bill with ID {pathology_bill_id} not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = PathologyBillSerializer(pathology, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user, tenant=request.tenant)
            return Response({"msg": "Pathology Bill updated successfully!"}, status=status.HTTP_200_OK)
        logger.error(f"Error while updating pathology bill: {serializer.errors}")
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )

    # DELETE: Delete specific pathology
    def delete(self, request, pathology_bill_id):
        try:
            if request.user.is_tenant_admin:
                pathology = PathologyBill.objects.get(id=pathology_bill_id)
            else:
                pathology = PathologyBill.objects.get(id=pathology_bill_id, user=request.user)
        except PathologyBill.DoesNotExist as e:
            logger.critical(f"Error deleting pathology bill: {e}")
            return Response(
                {"msg": f"Pathology Bill with ID {pathology_bill_id} not found or already deleted."},
                status=status.HTTP_404_NOT_FOUND,
            )

        pathology.delete()
        logger.info("Pathology Bill deleted successfully!")
        return Response({"msg": "Pathology Bill deleted successfully!"}, status=status.HTTP_200_OK)
