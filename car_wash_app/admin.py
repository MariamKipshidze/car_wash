from django.contrib import admin
from .models import EmployeeProfile, Location, Branch
from .models import CompanyProfile, Order, CarType
from .models import Car, Coupon, WashType, CompanyCarType


@admin.register(EmployeeProfile)
class EmployeeModelAdmin(admin.ModelAdmin):
    search_fields = ("full_name",)
    list_display = ["full_name", "branch", "manager", "order_percentage"]


@admin.register(Location)
class LocationModelAdmin(admin.ModelAdmin):
    search_fields = ("city",)
    list_display = ["city", "street_address"]
    

@admin.register(Branch)
class BranchModelAdmin(admin.ModelAdmin):
    search_fields = ("title",)
    list_display = ["company", "title", "location"]


@admin.register(CompanyProfile)
class CompanyProfileModelAdmin(admin.ModelAdmin):
    search_fields = ("company",)
    list_display = ["company", "mobile_number"]


@admin.register(CarType)
class CarTypeModelAdmin(admin.ModelAdmin):
    search_fields = ("model_type",)
    list_display = ["model_type"]


@admin.register(CompanyCarType)
class CompanyCarTypeModelAdmin(admin.ModelAdmin):
    search_fields = ("car_type",)
    list_display = ["car_type", "washing_cost", "company"]


@admin.register(Car)
class CarModelAdmin(admin.ModelAdmin):
    search_fields = ("licence_plate",)
    list_display = ["licence_plate", "car_type"]


@admin.register(Coupon)
class CouponModelAdmin(admin.ModelAdmin):
    search_fields = ("car_plate",)
    list_display = ["car", "code", "company", "discount", "expiration_date"]


@admin.register(WashType)
class WashTypeModelAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ["name", "percentage", "company"]


@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    search_fields = ("branch",)
    list_display = ["branch", "car", "start_date", "end_date"]