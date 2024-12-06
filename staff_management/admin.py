from django.contrib import admin

from .models import Role

admin.site.register(Role)


from .models import Employee

admin.site.register(Employee)
