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
    company = models.ForeignKey('Company', to_field="company_name",
    on_delete=models.CASCADE, null=True, blank=True)

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

    def __str__(self):
        return self.company_name

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

    def __str__(self):
        return f"{self.model_name} by {self.manufacturer}"

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
    owner = models.ForeignKey(Company, to_field="company_name",
                              on_delete=models.CASCADE)
    is_electrical = models.BooleanField(default=True)
    last_pat_test = models.DateField()
    last_calibration = models.DateField()

    def __str__(self):
        return self.manufacturer_reference

class Job(models.Model):
    """
    Class created for the active use of an asset with contact details.
    """

    STATUS_CHOICES = (
        ('none', 'none'),
        ('field_a', 'field_a'),
        ('field_b', 'field_b'),
        ('field_c', 'field_c'),
    )
    machine_id = models.ForeignKey(
        MachineProfile,
        to_field='manufacturer_reference',
        on_delete=models.CASCADE
    )
    created_by = models.CharField(max_length=250)
    start_date = models.DateField()
    job_status = models.CharField(max_length=100, 
                                  choices=STATUS_CHOICES,
                                  default='none')
    changed_by = models.CharField(max_length=250)
    changed_on = models.DateTimeField(auto_now=True)
    company_name = models.ForeignKey(
        Company,
        to_field="company_name",
        related_name="jobs",
        on_delete=models.CASCADE
    )
    contact = models.CharField(max_length=200, blank=True)
    po_reference = models.CharField(max_length=25, blank=True)

    def __str__(self):
        return f"Job {self.id} created by {self.created_by} of company\
        {self.company_name} using {self.machine_id}"
    

