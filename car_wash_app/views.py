from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Branch
from .forms import ProfileUpdateForm, UserUpdateForm


def home(request):
    context = {}
    branches = Branch.objects.all()
    context["branches"] = branches

    return render(request, "car_wash_app/home.html", context)


def detail(request, pk):
    branch = get_object_or_404(Branch, id=pk)
    return render(request, 'car_wash_app/branch_detail.html', context={
        'branch': branch
    })

@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"your account has been updated!")
            return redirect("profile")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)


    context = {
        "u_form": u_form,
        "p_form": p_form
    }

    return render(request, "car_wash_app/profile.html", context)