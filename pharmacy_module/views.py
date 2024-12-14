from django.db import IntegrityError
from elevenlabs import ValidationError
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from .models import MedicineList,PharmacyBill,PurchaseMedicine
from rest_framework.permissions import IsAuthenticated
from clients.custom_permissions import IsTenantAdminOrIsUserPartOfTenant
import logging

logger = logging.getLogger(__name__)

class MedicineListView(APIView):
    # permission_classes = [IsAuthenticated, IsTenantAdminOrIsUserPartOfTenant]

    # GET: List all medicine list for the tenant
    def get(self, request):
        
        MedicineList = MedicineList.objects.filter(tenant=request.tenant)
        
        serializer = MedicineListSerializer(MedicineList, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    # POST: Add a new MedicineList
    def post(self, request):
        serializer = MedicineListCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Save MedicineList with user and tenant
                serializer.save(user=request.user, tenant=request.tenant)
                return Response({"msg": "Medicine List added successfully!"}, status=status.HTTP_201_CREATED)
            except IntegrityError as e:
                raise ValidationError({"error": str(e)})
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class MedicineManagementView(APIView):
    permission_classes = [IsAuthenticated, IsTenantAdminOrIsUserPartOfTenant]

    def get(self, request, medicine_id):
        try:
            MedicineList = MedicineList.objects.get(id=medicine_id, tenant=request.tenant)
            serializer = MedicineListSerializer(MedicineList)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        except MedicineList.DoesNotExist:
            return Response({"msg": "Medicine List not found."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = MedicineListCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(tenant=request.tenant)
            return Response({"msg": "MedicineList added successfully!"}, status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, medicine_id):
        try:
            MedicineList = MedicineList.objects.get(id=medicine_id, tenant=request.tenant)
            serializer = MedicineListCreateUpdateSerializer(MedicineList, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"msg": "Medicine List updated successfully!"}, status=status.HTTP_200_OK)
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except MedicineList.DoesNotExist:
            return Response({"msg": "MedicineList not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, medicine_id):
        try:
            MedicineList = MedicineList.objects.get(id=medicine_id, tenant=request.tenant)
            MedicineList.delete()
            return Response({"msg": "Medicine List deleted successfully!"}, status=status.HTTP_200_OK)
        except MedicineList.DoesNotExist:
            return Response({"msg": "Medicine List not found."}, status=status.HTTP_404_NOT_FOUND)

    permission_classes = [IsAuthenticated, IsTenantAdminOrIsUserPartOfTenant]

   
    def get(self, request, medicine_id):
        try:
            # Tenant admin can access all medicine list, while users can only access their own medicine list
            if request.user.is_tenant_admin:
                MedicineList = MedicineList.objects.get(id=medicine_id)
            else:
                MedicineList = MedicineList.objects.get(id=medicine_id, user=request.user)
        except MedicineList.DoesNotExist as e:
            logger.critical(f"Error fetching medicine list: {e}")
            return Response(
                {"msg": f"Medicine List with ID {medicine_id} not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = MedicineListSerializer(MedicineList)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    # PATCH: Update specific medicine details
    def patch(self, request, medicine_id):
        try:
            if request.user.is_tenant_admin:
                MedicineList = MedicineList.objects.get(id=medicine_id)
            else:
                MedicineList = MedicineList.objects.get(id=medicine_id, user=request.user)
        except MedicineList.DoesNotExist as e:
            logger.critical(f"Error fetching Medicine List for update: {e}")
            return Response(
                {"msg": f"MedicineList with ID {medicine_id} not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = MedicineListSerializer(MedicineList, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user, tenant=request.tenant)
            return Response({"msg": "Medicine List updated successfully!"}, status=status.HTTP_200_OK)
        logger.error(f"Error while updating Medicine List: {serializer.errors}")
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )

    # DELETE: Delete specific MedicineList
    def delete(self, request, medicine_id):
        try:
            if request.user.is_tenant_admin:
                MedicineList = MedicineList.objects.get(id=medicine_id)
            else:
                MedicineList = MedicineList.objects.get(id=medicine_id, user=request.user)
        except MedicineList.DoesNotExist as e:
            logger.critical(f"Error deleting MedicineList: {e}")
            return Response(
                {"msg": f"MedicineList with ID {medicine_id} not found or already deleted."},
                status=status.HTTP_404_NOT_FOUND,
            )

        MedicineList.delete()
        logger.info("Medicine List deleted successfully!")
        return Response({"msg": "Medicine List deleted successfully!"}, status=status.HTTP_200_OK)
   
   
    
    
class PharmacyBillListView(APIView):
    # permission_classes = [IsAuthenticated, IsTenantAdminOrIsUserPartOfTenant]

    # GET: List all pharmacy_bill for the tenant
    def get(self, request):
       
        pharmacy_bill = PharmacyBill.objects.filter(tenant=request.tenant)
        
        serializer = PharmacyBillSerializer(pharmacy_bill, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    # POST: Add a new MedicineList Bill
    def post(self, request):
        serializer = PharmacyBillCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Save MedicineList Bill with user and tenant
                serializer.save(user=request.user, tenant=request.tenant)
                return Response({"msg": "Pharmacy Bill added successfully!"}, status=status.HTTP_201_CREATED)
            except IntegrityError as e:
                raise ValidationError({"error": str(e)})
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class PharmacyBillManagementView(APIView):
    permission_classes = [IsAuthenticated, IsTenantAdminOrIsUserPartOfTenant]

    def get(self, request, pharmacy_bill_id):
        try:
            pharmacy_bill = PharmacyBill.objects.get(id=pharmacy_bill_id, tenant=request.tenant)
            serializer = PharmacyBillSerializer(pharmacy_bill)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        except PharmacyBill.DoesNotExist:
            return Response({"msg": "Pharmacy Bill not found."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = PharmacyBillCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(tenant=request.tenant)
            return Response({"msg": "Pharmacy Bill added successfully!"}, status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pharmacy_bill_id):
        try:
            pharmacy_bill = PharmacyBill.objects.get(id=pharmacy_bill_id, tenant=request.tenant)
            serializer = PharmacyBillCreateUpdateSerializer(pharmacy_bill, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"msg": "Pharmacy Bill updated successfully!"}, status=status.HTTP_200_OK)
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except PharmacyBill.DoesNotExist:
            return Response({"msg": "Pharmacy Bill not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pharmacy_bill_id):
        try:
            pharmacy_bill = PharmacyBill.objects.get(id=pharmacy_bill_id, tenant=request.tenant)
            pharmacy_bill.delete()
            return Response({"msg": "Pharmacy Bill deleted successfully!"}, status=status.HTTP_200_OK)
        except PharmacyBill.DoesNotExist:
            return Response({"msg": "Pharmacy Bill not found."}, status=status.HTTP_404_NOT_FOUND)

    permission_classes = [IsAuthenticated, IsTenantAdminOrIsUserPartOfTenant]

   
    def get(self, request, pharmacy_bill_id):
        try:
            # Tenant admin can access all pharmacy_bill, while users can only access their own pharmacy_bill
            if request.user.is_tenant_admin:
                pharmacy_bill = PharmacyBill.objects.get(id=pharmacy_bill_id)
            else:
                pharmacy_bill = PharmacyBill.objects.get(id=pharmacy_bill_id, user=request.user)
        except PharmacyBill.DoesNotExist as e:
            logger.critical(f"Error fetching pharmacy bill: {e}")
            return Response(
                {"msg": f"Pharmacy Bill with ID {pharmacy_bill_id} not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = PharmacyBillSerializer(pharmacy_bill)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    # PATCH: Update specific pharmacy details
    def patch(self, request, pharmacy_bill_id):
        try:
            if request.user.is_tenant_admin:
                pharmacy_bill = PharmacyBill.objects.get(id=pharmacy_bill_id)
            else:
                pharmacy_bill = PharmacyBill.objects.get(id=pharmacy_bill_id, user=request.user)
        except PharmacyBill.DoesNotExist as e:
            logger.critical(f"Error fetching pharmacy bill for update: {e}")
            return Response(
                {"msg": f"Pharmacy Bill with ID {pharmacy_bill_id} not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = PharmacyBillSerializer(pharmacy_bill, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user, tenant=request.tenant)
            return Response({"msg": "Pharmacy Bill updated successfully!"}, status=status.HTTP_200_OK)
        logger.error(f"Error while updating pharmacy bill: {serializer.errors}")
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )

    # DELETE: Delete specific pharmacy
    def delete(self, request, pharmacy_bill_id):
        try:
            if request.user.is_tenant_admin:
                pharmacy_bill = PharmacyBill.objects.get(id=pharmacy_bill_id)
            else:
                pharmacy_bill = PharmacyBill.objects.get(id=pharmacy_bill_id, user=request.user)
        except PharmacyBill.DoesNotExist as e:
            logger.critical(f"Error deleting pharmacy bill: {e}")
            return Response(
                {"msg": f"Pharmacy Bill with ID {pharmacy_bill_id} not found or already deleted."},
                status=status.HTTP_404_NOT_FOUND,
            )

        pharmacy_bill.delete()
        logger.info("Pharmacy Bill deleted successfully!")
        return Response({"msg": "Pharmacy Bill deleted successfully!"}, status=status.HTTP_200_OK)




class PurchaseMedicineView(APIView):
    # permission_classes = [IsAuthenticated, IsTenantAdminOrIsUserPartOfTenant]

    # GET: List all medicine list for the tenant
    def get(self, request):
        
        PurchaseMedicine = PurchaseMedicine.objects.filter(tenant=request.tenant)
        
        serializer = MedicineListSerializer(PurchaseMedicine, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    # POST: Add a new MedicineList
    def post(self, request):
        serializer = MedicineListCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Save MedicineList with user and tenant
                serializer.save(user=request.user, tenant=request.tenant)
                return Response({"msg": "Purchase Medicine added successfully!"}, status=status.HTTP_201_CREATED)
            except IntegrityError as e:
                raise ValidationError({"error": str(e)})
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class PurchaseMedicineManagementView(APIView):
    permission_classes = [IsAuthenticated, IsTenantAdminOrIsUserPartOfTenant]

    def get(self, request, medicine_id):
        try:
            PurchaseMedicine = PurchaseMedicine.objects.get(id=medicine_id, tenant=request.tenant)
            serializer = PurchaseMedicineSerializer(PurchaseMedicine)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        except PurchaseMedicine.DoesNotExist:
            return Response({"msg": "Purchase Medicine not found."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = PurchaseMedicineCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(tenant=request.tenant)
            return Response({"msg": "Purchase Medicine added successfully!"}, status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, purchase_medicine_id):
        try:
            PurchaseMedicine = PurchaseMedicine.objects.get(id=purchase_medicine_id, tenant=request.tenant)
            serializer = PurchaseMedicineCreateUpdateSerializer(PurchaseMedicine, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"msg": "Purchase Medicine updated successfully!"}, status=status.HTTP_200_OK)
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except MedicineList.DoesNotExist:
            return Response({"msg": "Purchase Medicine not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, purchase_medicine_id):
        try:
            PurchaseMedicine = PurchaseMedicine.objects.get(id=purchase_medicine_id, tenant=request.tenant)
            PurchaseMedicine.delete()
            return Response({"msg": "Purchase Medicine deleted successfully!"}, status=status.HTTP_200_OK)
        except PurchaseMedicine.DoesNotExist:
            return Response({"msg": "Purchase Medicine not found."}, status=status.HTTP_404_NOT_FOUND)

    permission_classes = [IsAuthenticated, IsTenantAdminOrIsUserPartOfTenant]

   
    def get(self, request, purchase_medicine_id):
        try:
            # Tenant admin can access all medicine list, while users can only access their own medicine list
            if request.user.is_tenant_admin:
                PurchaseMedicine = PurchaseMedicine.objects.get(id=purchase_medicine_id)
            else:
                PurchaseMedicine = PurchaseMedicine.objects.get(id=purchase_medicine_id, user=request.user)
        except PurchaseMedicine.DoesNotExist as e:
            logger.critical(f"Error fetching Purchase Medicine list: {e}")
            return Response(
                {"msg": f"Purchase Medicine with ID {purchase_medicine_id} not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = PurchaseMedicineSerializer(PurchaseMedicine)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    # PATCH: Update specific purchase medicine details
    def patch(self, request, purchase_medicine_id):
        try:
            if request.user.is_tenant_admin:
                PurchaseMedicine = PurchaseMedicine.objects.get(id=purchase_medicine_id)
            else:
                PurchaseMedicine = PurchaseMedicine.objects.get(id=purchase_medicine_id, user=request.user)
        except PurchaseMedicine.DoesNotExist as e:
            logger.critical(f"Error fetching Purchase Medicine for update: {e}")
            return Response(
                {"msg": f"Purchase Medicine with ID {purchase_medicine_id} not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = PurchaseMedicineSerializer(PurchaseMedicine, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user, tenant=request.tenant)
            return Response({"msg": "Purchase Medicine updated successfully!"}, status=status.HTTP_200_OK)
        logger.error(f"Error while updating Purchase Medicine: {serializer.errors}")
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )

    # DELETE: Delete specific Purchase Medicine
    def delete(self, request, purchase_medicine_id):
        try:
            if request.user.is_tenant_admin:
                PurchaseMedicine = PurchaseMedicine.objects.get(id=purchase_medicine_id)
            else:
                PurchaseMedicine = PurchaseMedicine.objects.get(id=purchase_medicine_id, user=request.user)
        except PurchaseMedicine.DoesNotExist as e:
            logger.critical(f"Error deleting Purchase Medicine: {e}")
            return Response(
                {"msg": f"Purchase Medicine with ID {purchase_medicine_id} not found or already deleted."},
                status=status.HTTP_404_NOT_FOUND,
            )

        PurchaseMedicine.delete()
        logger.info("Purchase Medicine deleted successfully!")
        return Response({"msg": "Purchase Medicine deleted successfully!"}, status=status.HTTP_200_OK)
   