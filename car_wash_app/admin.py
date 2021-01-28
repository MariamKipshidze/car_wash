from django.contrib import admin
from .models import Employee, Location, Branch
from .models import CompanyProfile, Order, Car


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


@admin.register(Car)
class CarModelAdmin(admin.ModelAdmin):
    search_fields = ("model_type",)
    list_display = ["id_number", "model_type", "washing_cost", ]


@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    search_fields = ("branch",)
    list_display = [ "branch", "customer", "order_date", "finish_date", ]