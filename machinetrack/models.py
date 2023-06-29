from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.contrib.postgres.fields import ArrayField
from django.dispatch import receiver
from phone_field import PhoneField
import datetime


# Create your models here.

class Profile(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    company = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

@receiver(post_save, sender=Profile.username)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=Profile.username)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Company(models.Model):
    """
    Allow user to create a company and add employees. This will act as a company view.
    """
    company_name = models.CharField(max_length=50, unique=True)
    company_image = models.FileField(upload_to='images/', 
                                      default="https://res.cloudinary.com/dz1h0duk6/image/upload/v1687467973/dr_box_buidea.png",
                                      )
    owner = models.ForeignKey(Profile,
                              related_name="+",
                               on_delete=models.CASCADE)
    employees = ArrayField(
        models.CharField(max_length=50, blank=True),
        size=10,
        blank=True
    )
    phone_number = PhoneField(blank=True, null=True)
    field_a = models.CharField(max_length=30, blank=False)
    field_b = models.CharField(max_length=30, blank=False)
    field_c = models.CharField(max_length=30, blank=False)
    pin = models.PositiveIntegerField(blank=False, default=0000)

class MachineModel(models.Model):
    """
    Users can create a new base detail of machines
    """
    manufacturer = models.CharField(max_length=50)
    model_name = models.CharField(unique=True, max_length=20, blank=False)
    fusion_type = models.CharField(max_length=25)
    voltage = models.PositiveIntegerField()
    image = models.FileField(upload_to = 'images/',
                             )
    manufacturer_product_code = models.CharField(max_length = 20)

class MachineProfile(models.Model):
    """
    Unique machine references linked with models above. These are indiviudal asset references
    """
    manufacturer_reference = models.CharField(unique=True, max_length=25, blank=False)
    company_reference = models.CharField(max_length=25, blank=True)
    model = models.ForeignKey(MachineModel, to_field="model_name", on_delete=models.CASCADE)
    serial_number = models.CharField(max_length=30, unique=True)
    year_of_man = models.PositiveIntegerField()
    status = models.CharField(max_length=30)
    owner = models.CharField(max_length=30)
    is_electrical = models.BooleanField(default=True)
    last_pat_test = models.DateTimeField()
    last_calibration = models.DateTimeField()
