from django.urls import path
from django.urls.conf import include
from rest_framework import routers

from . import views

urlpatterns = [
    path('', views.api_overview, name="API Overviews"),
    path('api/contacts', views.list_contact, name="List Contact" ),
    path('api/contacts/<str:id>', views.detail_contact, name="Detail Contact"),
    path('api/contacts/create', views.create_contact, name="Create Contact")
]