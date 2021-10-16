from django.contrib import admin

from application.models.contact import Contact
from application.models.contact_list import ContactList

# Register your models here.

admin.site.register(Contact)
admin.site.register(ContactList)