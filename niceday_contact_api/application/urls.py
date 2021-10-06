from django.urls import path
from django.urls.conf import include
from rest_framework import routers

from . import views

urlpatterns = [
    path('', views.api_overview, name="API Overviews"),
    path('api/contacts', views.list_contacts, name="List Contact" ),
    path('api/contacts/create', views.create_contact, name="Create Contact"),
    path('api/contacts/delete', views.delete_contact, name="Delete Contact")
]