from django.urls import path
from django.urls.conf import include
from rest_framework import routers

from . import views

urlpatterns = [
    path('', views.api_overview, name="API Overviews"),
    path('api/contacts', views.contact_view, name="Contact View" ),
    path('api/contacts/<str:id>', views.single_contact_view, name="Single Contact View"),
    path('api/contact-lists', views.contact_list_view, name="Contact List View"),
    path('api/contact-lists/<str:id>', views.single_contact_list_view, name="Single Contact List View"),
    path('api/contact-lists/<str:list_id>/contacts', views.assigned_contact_view, name="Assigned Contact View")
]