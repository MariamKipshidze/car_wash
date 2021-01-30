from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.constraints import UniqueConstraint
from django.db.models.query_utils import Q
from user.models import User
from PIL import Image

class Location(models.Model):
    city = models.CharField(max_length = 255, verbose_name = _("City"))
    street_address = models.CharField(max_length = 255, verbose_name = _('Street Address'))

    def __str__(self):
        return f'{self.city} : {self.street_address}'

    class Meta:
        unique_together = ['city', 'street_address']

     
class Branch(models.Model):
    company = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Company"))
    title = models.CharField(max_length = 255, verbose_name=_('Branch'))
    location = models.OneToOneField(Location, on_delete = models.PROTECT, verbose_name = _("Location"))
    description = models.TextField(verbose_name=_("Description"))
    image = models.ImageField(null = True, blank = True, upload_to = "pictures", verbose_name=_("Image"))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Branch')
        verbose_name_plural = _('Branches')


class EmployeeProfile(models.Model):
    employee = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_("Employee"))
    full_name = models.CharField(_("Full Name"), max_length = 255)
    age = models.PositiveSmallIntegerField(_("Age"))
    mobile_number = models.CharField(max_length=20, verbose_name=_("Mobile Number"))
    manager = models.BooleanField(default = False, verbose_name = _("Manager"))
    branch = models.ForeignKey(Branch, on_delete = models.CASCADE, verbose_name = _("Branch"), related_name="branch")
    salary = models.DecimalField(max_digits=8, decimal_places=2, verbose_name=_('Salary'), help_text='in Lari')

    class Meta:
        constraints = [
            UniqueConstraint(fields=['branch'], condition=Q(manager=True), name = "unique_together_manager_branch")
        ]
        
    def __str__(self):
        return self.full_name


class CompanyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_("Company"))
    image = models.ImageField(default="default_logo.jpg", upload_to="logo_pics", verbose_name=_("Image"))

    def __str__(self):
        return f"{self.user.username} Profile"

    def save(self, *args, **kwargs):
        super(CompanyProfile, self).save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class CarType(models.Model):
    model_type = models.CharField(_("Car Model"), max_length=100)
    washing_cost = models.SmallIntegerField(_("Cost"))

    def __str__(self):
        return self.model_type

    class Meta:
        verbose_name = _('Car')
        verbose_name_plural = _('Cars')


class WashType(models.Model):
    name = models.CharField(max_length=45, verbose_name=_('Car Type'), unique=True)
    percentage = models.IntegerField(verbose_name=_("Percentage of base price"), default=100)

    def __str__(self):
        return self.name


class Coupon(models.Model):
    code = models.CharField(max_length=30, unique=True)
    expiration_date = models.DateTimeField(verbose_name=_('Coupon Expiration Date'), null=True, blank=True)
    discount = models.IntegerField(verbose_name=_('Discount'), help_text='%')
    quantity = models.IntegerField(verbose_name=_('Quantity'), default=1)
    car_plate = models.CharField(max_length=20, verbose_name=_("Car's license plate"))

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = _('Coupon')
        verbose_name_plural = _('Coupons')


class Car(models.Model):
    car_type = models.ForeignKey(
        to='CarType',
        on_delete=models.SET_NULL,
        null=True, related_name='cars'
    )
    licence_plate = models.CharField(max_length=20, verbose_name=_("License plate"))

    def __str__(self):
        return self.licence_plate

    class Meta:
        verbose_name = _('Car')
        verbose_name_plural = _('Cars')


class Order(models.Model):
    car = models.ForeignKey(
        to='Car', related_name='orders',
        on_delete=models.PROTECT,
    )
    employee = models.ForeignKey(
        to='EmployeeProfile', on_delete=models.SET_NULL,
        null=True, related_name='orders',
    )
    coupon = models.ForeignKey(
        to='Coupon', related_name='orders',
        on_delete=models.PROTECT,
        null=True, blank=True,
    )
    wash_type = models.ForeignKey(
        to='WashType', related_name='orders',
        on_delete=models.PROTECT,
    )

    note = models.TextField(null=True, blank=True, verbose_name=_("Note"))
    price = models.DecimalField(max_digits=4, decimal_places=2, verbose_name=_("Price"))

    created_date = models.DateTimeField(auto_now_add=True, verbose_name=_("Created date"))
    start_date = models.DateTimeField(verbose_name=_('Scheduled time'))
    end_date = models.DateTimeField(verbose_name=_('Scheduled time'))

    def __str__(self):
        return f'{self.car} using {self.wash_type}'

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def save(self, *args, **kwargs):
        if not self.pk:
            self.price = self.car.car_type.price * self.wash_type.percentage / 100
        super(Order, self).save(*args, **kwargs)



