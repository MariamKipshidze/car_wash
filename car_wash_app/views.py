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