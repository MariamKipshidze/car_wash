from django.db.models.signals import post_save
from user.models import User
from django.dispatch import receiver
from .models import CompanyProfile

@receiver(post_save, sender =  User)
def create_company_profile(sender, instance, created, **kwargs):
    if created and instance.status == 1:
        CompanyProfile.objects.create(company = instance)


@receiver(post_save, sender =  User)
def save_company_profile(sender, instance,  **kwargs):
    instance.company.save()