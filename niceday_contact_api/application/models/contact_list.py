from django.db import models
from uuid import uuid4

from application.models.contact import Contact

class ContactList(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=64, null=False)
    description = models.CharField(max_length=256, blank=True, null=True)
    contacts = models.ManyToManyField(Contact)