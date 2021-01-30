import datetime 
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Branch, EmployeeProfile, Order
from .forms import ProfileUpdateForm, UserUpdateForm, OrderForm
from .forms import CompanyRegisterForm, OrderFilterChoice
from django.utils import timezone
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.urls import reverse


def home(request):
    branches = Branch.objects.all()
    return render(request, "car_wash_app/home.html", context = {
        "branches":branches
    })


def detail(request, pk):
    branch = get_object_or_404(Branch, id=pk)
    employees = branch.branch.all()
    order_form = OrderForm(branch)

    if request.method == "POST":
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order = order_form.save(commit=False)

            order_date = order_form.cleaned_data["order_date"]
            order.end_date = order_date + datetime.timedelta(minutes = 30)

            order.branch = branch

            order_form.save()
            messages.success(request, f"Successfully booked!")
            return HttpResponseRedirect(reverse("branch-detail", args=[str(pk)]))

    return render(request, 'car_wash_app/branch_detail.html', context={
        'branch': branch,
        'employees': employees,
        'order_form': order_form
    })


@login_required
def employee_profile(request, pk):
    employee = get_object_or_404(EmployeeProfile, id=pk)
    orders  = employee.order.all().count()
    order_search_form = OrderFilterChoice()

    if request.method == "POST":
        orders = order_search_form.cleaned_data["order_search"]
        if orders == 1:
            orders = employee.order.filter(order_date__gte = (timezone.now() - datetime.timedelta(weeks=1)))
        elif orders == 2:
            orders = employee.order.filter(order_date__gte = (timezone.now() - datetime.timedelta(days=30)))
        elif orders == 3:
            orders = employee.order.filter(order_date__gte = (timezone.now() - datetime.timedelta(days=365)))
        return HttpResponseRedirect(reverse("employee-detail", args=[str(pk)]))

    return render(request, 'car_wash_app/employee_detail.html', context={
        'employee': employee,
        'orders': orders,
        'order_search_form':order_search_form,
    })


@login_required
def profile(request):
    user_update_form = UserUpdateForm(instance=request.user)
    profile_update_form = ProfileUpdateForm(instance=request.user.companyprofile)

    if request.method == "POST":
        user_update_form = UserUpdateForm(request.POST, instance=request.user)
        profile_update_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.companyprofile)

        if user_update_form.is_valid() and profile_update_form.is_valid():
            user_update_form.save()
            profile_update_form.save()
            messages.success(request, f"your account has been updated!")
            return redirect("profile")


    context = {
        "user_update_form": user_update_form,
        "profile_update_form": profile_update_form
    }

    return render(request, "car_wash_app/profile.html", context)

def company_register(request):
    company_register_form = CompanyRegisterForm()
    if request.method == "POST":
        company_register_form = CompanyRegisterForm(request.POST)
        if company_register_form.is_valid():
            company_register_form.save()
            messages.success(request, f"Account created successfully!")
            return redirect("login")

    return render(request, "car_wash_app/company_register.html",context={
        "company_register_form": company_register_form
        })


@login_required
def employee_register(request):
    pass