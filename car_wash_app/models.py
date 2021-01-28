from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.constraints import UniqueConstraint
from django.db.models.query_utils import Q
from django.contrib.auth.models import User
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
        verbose_name = 'Branch'
        verbose_name_plural = 'Branches'


class Employee(models.Model):
    full_name = models.CharField(_("Full Name"), max_length = 255)
    age = models.PositiveSmallIntegerField(_("Age"))
    mobile_number = models.CharField(max_length=20, verbose_name=_("Mobile Number"))
    manager = models.BooleanField(default = False, verbose_name = _("Manager"))
    branch = models.ForeignKey(Branch, on_delete = models.CASCADE, verbose_name = _("Branch"), related_name="branch")

    class Meta:
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'
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


class Car(models.Model):
    id_number = models.SmallIntegerField(_("ID Number"))
    model_type = models.CharField(_("Car Model"), max_length=100)
    washing_cost = models.SmallIntegerField(_("Cost"))

    def __str__(self):
        return self.model_type

    class Meta:
        verbose_name = 'Car'
        verbose_name_plural = 'Cars'


class Order(models.Model):
    customer = models.CharField(max_length=100, verbose_name=_("Customer"))
    branch = models.ForeignKey(Branch, verbose_name=_("Branch"), on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    finish_date = models.DateTimeField()
    employee = models.ForeignKey(Employee, verbose_name=_("Employee"), on_delete=models.PROTECT, related_name="order")
    car = models.ForeignKey(Car, verbose_name=_("Car"), on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        unique_together = ['employee', 'order_date']

    def __str__(self):
        return self.customer



