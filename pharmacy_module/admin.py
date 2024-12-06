from django.contrib import admin


from .models import PharmacyBill

admin.site.register(PharmacyBill)


from .models import MedicineList

admin.site.register(MedicineList)

from .models import PurchaseMedicine

admin.site.register(PurchaseMedicine)