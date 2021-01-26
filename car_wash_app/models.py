from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.constraints import UniqueConstraint
from django.db.models.query_utils import Q


class Location(models.Model):
    city = models.CharField(max_length = 255, verbose_name = _("City"))
    street_address = models.CharField(max_length = 255, verbose_name = _('Street Address'))

    def __str__(self):
        return f'{self.city} : {self.street_address}'

    class Meta:
        unique_together = ['city', 'street_address']

     
class Branch(models.Model):
    title = models.CharField(max_length = 255, verbose_name=_('Branch'))
    location = models.OneToOneField(Location, on_delete = models.PROTECT, verbose_name = _("Location"))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Branch'
        verbose_name_plural = 'Branches'


class Employee(models.Model):
    full_name = models.CharField(_("Full Name"), max_length = 255)
    age = models.PositiveSmallIntegerField(_("Age"))
    manager = models.BooleanField(default = False, verbose_name = _("Manager"))
    branch = models.ForeignKey(Branch, on_delete = models.CASCADE, verbose_name = _("Branch"))

    class Meta:
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'
        constraints = [
            UniqueConstraint(fields=['branch'], condition=Q(manager=True), name = "unique_together_manager_branch")
        ]
        
    def __str__(self):
        return self.full_name