from django.core import validators
from django.db import models
from django.core.validators import RegexValidator
from uuid import uuid4

PHONE_REGEX = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

class Contact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=64, null=False)
    email = models.EmailField(max_length=320, null=False)
    address = models.CharField(max_length=512, blank=True, null=True)
    phone_number = models.CharField(max_length=16, validators = [PHONE_REGEX], blank=True, null=True)

    def __str__(self):
        return self.name
