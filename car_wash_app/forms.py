from django import forms
from user.models import User
from .models import CompanyProfile, Order, EmployeeProfile, Car, WashType
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MaxLengthValidator, MinLengthValidator, RegexValidator
from django.forms import EmailField, CharField, Textarea, ModelChoiceField, TextInput


class OrderForm(forms.ModelForm):
    def __init__(self, current_company, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['branch'].queryset = self.fields['branch'].queryset.filter(company = current_company)
        self.fields['employee'].queryset = self.fields['employee'].queryset.filter(branch__company = current_company)
    
    note = CharField(widget=Textarea(attrs={
    'id': 'icon_prefix2',
    'class': 'materialize-textarea'
    }), validators=[MaxLengthValidator(150)])
    car = ModelChoiceField(empty_label='აირჩიე მანქანა', queryset=Car.objects.all())
    wash_type = ModelChoiceField(queryset=WashType.objects.all(), empty_label='აირჩიე რეცხვის ტიპი')
    start_date_day = CharField(widget=TextInput(attrs={
        'class': 'datepicker'
    }), validators=[RegexValidator(
        r'^((21|20)\d\d)[-](0[1-9]|1[012])[-](0[1-9]|[12][0-9]|3[01])$',
        message='ფორმატი უნდა იყოს: yyyy-mm-dd'
    )])
    start_date_time = CharField(widget=TextInput(attrs={
        'class': 'timepicker'
    }), validators=[RegexValidator(r'^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$', message='ფორმატი უნდა იყოს: HH:MM')])


    class Meta:
        model = Order
        fields = ('branch', 'employee', 'car', "wash_type", 'start_date_day', 'start_date_time', "note", )


# class OrderForm(forms.ModelForm):
#     def __init__(self, current_company, *args, **kwargs):
#         super(OrderForm, self).__init__(*args, **kwargs)
#         self.fields['branch'].queryset = self.fields['branch'].queryset.filter(company = current_company)
#         self.fields['employee'].queryset = self.fields['employee'].queryset.filter(branch__company = current_company)


#     note = CharField(widget=Textarea(attrs={
#         'id': 'icon_prefix2',
#         'class': 'materialize-textarea'
#     }), validators=[MaxLengthValidator(150)])
#     car = ModelChoiceField(empty_label='აირჩიე მანქანა', queryset=Car.objects.all())
#     wash_type = ModelChoiceField(queryset=WashType.objects.all(), empty_label='აირჩიე რეცხვის ტიპი')
#     start_date_day = CharField(widget=TextInput(attrs={
#         'class': 'datepicker'
#     }), validators=[RegexValidator(
#         r'^(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](21|20)\d\d$',
#         message='ფორმატი უნდა იყოს: dd/mm/yyyy'
#     )])
#     start_date_time = CharField(widget=TextInput(attrs={
#         'class': 'timepicker'
#     }), validators=[RegexValidator(r'^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$', message='ფორმატი უნდა იყოს: MM:HH')])


#     class Meta:
#         model = Order
#         fields = ('branch', 'employee','car', "wash_type", 'start_date_day', 'start_date_time',)


class OrderSearchForm(forms.Form):
    CHOICE = (("1", "last week"), ("2", "last month"), ("3", "last year") )
    order_search = forms.ChoiceField(choices=CHOICE, required=False)


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
        fields = ["full_name", "age", "mobile_number", "manager", "salary","order_percentage",]


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email"]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        fields = ["image", "mobile_number",]

