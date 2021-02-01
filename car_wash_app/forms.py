from django import forms
from user.models import User
from .models import CompanyProfile, Order, EmployeeProfile
from django.contrib.auth.forms import UserCreationForm


class OrderSearchForm(forms.Form):
    CHOICE = (("1", "last week"), ("2", "last month"), ("3", "last year") )
    order_search = forms.ChoiceField(choices=CHOICE)


class CompanyRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = [ "email", "password1", "password2"]


class EmployeeRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = [ "email", "status", "password1", "password2",]


class EmployeeProfileRegisterForm(forms.ModelForm):
    class Meta:
        model = EmployeeProfile
        fields = ["employee", "full_name", "age", "mobile_number", "manager", "salary","order_percentage",]


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email"]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        fields = ["image", "mobile_number",]


class OrderForm(forms.ModelForm):
    def __init__(self, current_branch, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['employee'].queryset = self.fields['employee'].queryset.filter(branch = current_branch)

    class Meta:
        model = Order
        fields = ('start_date', 'employee', 'car', "coupon", "wash_type")