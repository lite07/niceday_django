from django.urls import path
from django.urls.conf import include
from rest_framework import routers

from . import views

urlpatterns = [
    path('', views.api_overview, name="API Overviews"),
    path('api/contacts', views.contact_view, name="List Contact" ),
    path('api/contacts/<str:id>', views.single_contact_view, name="Detail Contact")
]