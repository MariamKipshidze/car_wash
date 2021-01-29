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
    def __init__(self, current_branch, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['employee'].queryset = self.fields['employee'].queryset.filter(branch = current_branch)


    class Meta:
        model = Order
        fields = ('customer', 'order_date', 'employee', 'car',)