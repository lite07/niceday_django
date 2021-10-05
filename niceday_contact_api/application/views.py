from django.shortcuts import render
from rest_framework import viewsets
from application.models.contact import Contact
from application.serializers import ContactSerializer

class ContactView(viewsets.ModelViewSet):
    serializer_class = ContactSerializer
    queryset = Contact.objects.all()
