from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(CelloTypes, CustomerMaster, Processed, OrderTable, loginTable, usersTable, tempTableProcess, tempTableOrder)
class ViewAdmin(admin.ModelAdmin):
    pass
