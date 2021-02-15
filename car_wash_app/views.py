import datetime 
from decimal import Decimal
from django.db.models import F, Sum, ExpressionWrapper, DecimalField, Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView, DeleteView

from .models import Branch, CompanyProfile, CompanyCarType, Coupon, Car
from .forms import ProfileUpdateForm, UserUpdateForm, CompanyRegisterForm, OrderSearchForm
from .forms import EmployeeRegisterForm, EmployeeProfileRegisterForm, OrderForm, CarCreateForm
from .forms import CompanyCarTypeForm, WashTypeForm, LocationForm, BranchForm, CouponForm

from django.utils import timezone
from django.db.models import Count
from django.http import HttpResponseRedirect, HttpResponse
from django.core.handlers.wsgi import WSGIRequest
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def home(request: WSGIRequest) -> HttpResponse:
    branches = Branch.objects.all()
    q = request.GET.get('q')

    if q:
        branches = Branch.objects.filter(Q(company__name__icontains=q)|Q(title__icontains=q))

    page = request.GET.get('page', 1)
    paginator = Paginator(branches, 5)
    try:
        branches = paginator.page(page)
    except PageNotAnInteger:
        branches = paginator.page(1)
    except EmptyPage:
        branches = paginator.page(paginator.num_pages)

    return render(request, "car_wash_app/home.html", context={
        "branches": branches,
    })


def detail(request: WSGIRequest, pk: int) -> HttpResponse:
    branch = get_object_or_404(Branch, id=pk)
    car_type = CompanyCarType.objects.filter(company=branch.company)

    return render(request, 'car_wash_app/branch_detail.html', context={
        'branch': branch,
        'car_type': car_type,
    })


@login_required
def employee_profile(request: WSGIRequest) -> HttpResponse:
    employee = request.user.employeeprofile
    order_search_form = OrderSearchForm()
    orders = employee.orders.order_by("-start_date")

    earned_money_q = ExpressionWrapper(
        F('price') * F('employee__order_percentage') / Decimal('100.0'),
        output_field=DecimalField())

    def employeeinfo(x):
        employee_info = employee.orders.filter(end_date__lte=timezone.now()) \
            .annotate(earned_per_order=earned_money_q) \
            .aggregate(
            earned_money=Sum(
                'earned_per_order',
                filter=Q(start_date__gte=(timezone.now() - x))
            ),
            washed_amount=Count(
                'id',
                filter=Q(start_date__gte=(timezone.now() - x))
            ))
        return employee_info

    employee_info = {}

    if request.method == "GET":
        order_search_form = OrderSearchForm(request.GET)
        if order_search_form.is_valid():
            data = order_search_form.cleaned_data["order_search"]
            if data == "1":
                orders = employee.orders.filter(start_date__gte=(timezone.now()\
                - datetime.timedelta(weeks=1))).order_by("-start_date")
                employee_info = employeeinfo(datetime.timedelta(days=7))
            elif data == "2":
                orders = employee.orders.filter(start_date__gte=(timezone.now()\
                 - datetime.timedelta(days=30))).order_by("-start_date")
                employee_info = employeeinfo(datetime.timedelta(days=30))
            elif data == "3":
                orders = employee.orders.filter(start_date__gte=(timezone.now()\
                 - datetime.timedelta(days=365))).order_by("-start_date")
                employee_info = employeeinfo(datetime.timedelta(days=365))
    
    return render(request, 'car_wash_app/employee_detail.html', context={
        "employee": employee,
        "order_search_form": order_search_form,
        "orders": orders,
        **employee_info
    })


@login_required
def profile(request: WSGIRequest) -> HttpResponse:
    company = request.user.company
    branches = company.branch.all()
    user_update_form = UserUpdateForm(instance=request.user)
    profile_update_form = ProfileUpdateForm(instance=request.user.company)

    if request.method == "POST":
        user_update_form = UserUpdateForm(request.POST, instance=request.user)
        profile_update_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user.company)

        if user_update_form.is_valid() and profile_update_form.is_valid():
            user_update_form.save()
            profile_update_form.save()
            messages.success(request, f"your account has been updated!")
            return redirect("profile")

    context = {
        "user_update_form": user_update_form,
        "profile_update_form": profile_update_form,
        "branches": branches,
    }

    return render(request, "car_wash_app/profile.html", context)


def company_register(request: WSGIRequest) -> HttpResponse:
    company_register_form = CompanyRegisterForm()
    if request.method == "POST":
        company_register_form = CompanyRegisterForm(request.POST)
        if company_register_form.is_valid():
            company_register_form.save()
            messages.success(request, f"Account created successfully!")
            return redirect("login")

    return render(request, "car_wash_app/company_register.html", context={
        "company_register_form": company_register_form
        })


@login_required
def employee_register(request: WSGIRequest, pk: int) -> HttpResponse:
    branch = get_object_or_404(Branch, id=pk)
    employee_register_form = EmployeeRegisterForm()
    employee_profile_register_form = EmployeeProfileRegisterForm()

    if request.method == "POST":
        employee_register_form = EmployeeRegisterForm(request.POST)
        employee_profile_register_form = EmployeeProfileRegisterForm(request.POST)
        if employee_register_form.is_valid() and employee_profile_register_form.is_valid():
            employee = employee_register_form.save()
            employee_profile = employee_profile_register_form.save(commit=False)

            employee_profile.branch = branch
            employee_profile.employee = employee
            employee_profile.save()
            
            messages.success(request, f"The employee profile was successfully created")
            return HttpResponseRedirect(reverse("employee-register", args=[str(pk)]))

    return render(request, "car_wash_app/employee_register.html", context={
        "employee_register_form": employee_register_form,
        "employee_profile_register_form": employee_profile_register_form,
        "branch": branch,
        })


@login_required
def order_create(request: WSGIRequest) -> HttpResponse:
    company = get_object_or_404(CompanyProfile, id=request.user.company.pk)
    order_form = OrderForm(company)

    if request.method == "POST":
        order_form = OrderForm(company, request.POST)
        if order_form.is_valid():
            order = order_form.save(commit=False)

            wash_type_percentage = order_form.cleaned_data["wash_type"].percentage
            car_type = order_form.cleaned_data["car"].car_type

            car_type_price = get_object_or_404(CompanyCarType, company=company, car_type=car_type).washing_cost
            order.start_date = order_form.cleaned_data["start_date_day"] + \
            " " + order_form.cleaned_data["start_date_time"]
            car = order_form.cleaned_data["car"]
            employee = order_form.cleaned_data["employee"]
            order.employee_order_percentage = employee.order_percentage

            order.price = (wash_type_percentage*car_type_price)/100

            if Coupon.objects.filter(Q(car=car),Q(company=company)).exists():
                coupons = Coupon.objects.filter(Q(car=car),Q(company=company))
                for coupon in coupons:
                    if coupon.quantity != 0 and coupon.expiration_date > timezone.now():
                        coupon.quantity = coupon.quantity - 1
                        coupon.save()
                        order.price = (order.price*(100-coupon.discount))/100

            order.save()

            messages.success(request, f"Successfully booked")
            return HttpResponseRedirect(reverse("order-create"))

    return render(request, "car_wash_app/order_form.html", context={
        "order_form": order_form,
        })


def car_create(request: WSGIRequest) -> HttpResponse:
    car_form = CarCreateForm()

    if request.method == "POST":
        car_form = CarCreateForm(request.POST)
        if car_form.is_valid():
            car_form.save()

            messages.success(request, f"Successfully created")
            return HttpResponseRedirect(reverse("home"))

    return render(request, "car_wash_app/car_form.html", context={
        "car_form": car_form,
        })


@login_required
def company_car_type_create(request: WSGIRequest) -> HttpResponse:
    company_car_type_form = CompanyCarTypeForm()

    if request.method == "POST":
        company_car_type_form = CompanyCarTypeForm(request.POST)
        if company_car_type_form.is_valid():
            company_car_type = company_car_type_form.save(commit=False)
            company_car_type.company = request.user.company
            company_car_type.save()

            messages.success(request, f"Successfully created")
            return HttpResponseRedirect(reverse("home"))

    return render(request, "car_wash_app/company_car_type_form.html", context={
        "company_car_type_form": company_car_type_form,
        })


@login_required
def wash_type_create(request: WSGIRequest) -> HttpResponse:
    wash_type_form = WashTypeForm()

    if request.method == "POST":
        wash_type_form = WashTypeForm(request.POST)
        if wash_type_form.is_valid():
            wash_type = wash_type_form.save(commit=False)
            wash_type.company = request.user.company
            wash_type.save()

            messages.success(request, f"Successfully created")
            return HttpResponseRedirect(reverse("home"))

    return render(request, "car_wash_app/wash_type_form.html", context={
        "wash_type_form": wash_type_form,
        })


@login_required
def branch_create(request: WSGIRequest) -> HttpResponse:
    branch_form = BranchForm()
    location_form = LocationForm()

    if request.method == "POST":
        branch_form = BranchForm(request.POST)
        location_form = LocationForm(request.POST)
        if location_form.is_valid() and location_form.is_valid():
            location = location_form.save()
            branch = branch_form.save(commit=False)
            branch.location = location 
            branch.company = request.user.company
            branch.save()

            messages.success(request, f"Successfully created")
            return HttpResponseRedirect(reverse("home"))

    return render(request, "car_wash_app/branch_form.html", context={
        "branch_form": branch_form,
        "location_form": location_form,
        })


class CouponCreateView(LoginRequiredMixin, CreateView):
    form_class = CouponForm
    template_name = 'car_wash_app/coupon_form.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.company = self.request.user.company
        messages.success(self.request, f"Coupon created successfully!")
        return super().form_valid(form)


class BranchDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Branch
    success_url = "/"

    def test_func(self):
        branch = self.get_object()
        if self.request.user.company == branch.company:
            return True
        return False
