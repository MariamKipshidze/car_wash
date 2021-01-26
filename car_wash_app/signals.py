from django.db.models.signals import post_save
from .models import User
from django.dispatch import receiver
from .models import CompanyProfile

@receiver(post_save, sender =  User)
def create_company_profile(sender, instance, created, **kwargs):
    if created:
        CompanyProfile.objects.create(user  = instance)


@receiver(post_save, sender =  User)
def save_company_profile(sender, instance,  **kwargs):
    instance.companyprofile.save()