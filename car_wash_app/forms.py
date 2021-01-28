from django import forms
from django.contrib.auth.models import User
from .models import CompanyProfile, Order


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', "email"]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        fields = ["image"]


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('order_date', 'employee', 'car',)