from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Branch


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
