from django import forms
from user.models import User
from .models import CompanyProfile, Order
from django.contrib.auth.forms import UserCreationForm


class CompanyRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = [ "email", "password1", "password2"]


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email"]


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
        fields = ('start_date', 'employee', 'car',)