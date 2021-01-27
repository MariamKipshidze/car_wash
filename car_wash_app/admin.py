from django.contrib import admin
from .models import Employee, Location, Branch
from .models import CompanyProfile


@admin.register(Employee)
class EmployeeModelAdmin(admin.ModelAdmin):
    search_fields = ("full_name",)
    list_display = ["full_name", "branch", "manager",]


@admin.register(Location)
class LocationModelAdmin(admin.ModelAdmin):
    search_fields = ("city",)
    list_display = ["city", "street_address",]
    

@admin.register(Branch)
class BranchModelAdmin(admin.ModelAdmin):
    search_fields = ("title",)
    list_display = ["company","title", "location",]


@admin.register(CompanyProfile)
class CompanyProfileModelAdmin(admin.ModelAdmin):
    search_fields = ("user",)
    list_display = ["user",]